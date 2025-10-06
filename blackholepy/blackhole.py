from dataclasses import dataclass, field
from datetime import timedelta
import warnings
import re as regex

from sympy import sqrt, Equality, solve

from blackholepy import formulas, config
from blackholepy.formulas import calculate, BlackHoleMetric, KerrMetric, KerrNewmanMetric, SchwarzschildMetric, ReissnerNordströmMetric
from blackholepy.symbols import *
from blackholepy.exceptions import *

def spin_param(spin: float, mass: float) -> float:
    "Calculate a black holes spin from its spin parameter"
    return calculate(formulas.dimensionless_spin, {a_star: spin, M: mass}, a)

@dataclass
class BlackHole():
    """Class representing a black hole.

    Parameters
    ----------
    mass : kilogram as float
    spin : meter as float
        The Metric required here is the 'Kerr-parameter' *a*, messured in meters.<br>
        Not to be confused with the spin parameter *a*<sub>*</sub> (between 0 and 1) or the angular momentum *J* (in kg m^2 / s).
    charge : coloumb as float

    Raises
    ----------
    CosmicCensorshipHypothesis : If parameters exceed certain limits, so that event horizons become imaginary
    LawOfConservationOfEnergy : If parameters cause behavior that would destroy energy or create it out of nothing
    """
        
    mass:   Float
    spin:   Float           = 0
    charge: Float           = 0
    metric: BlackHoleMetric = field(init=False)
    "Collection of formulas that descripe the black holes properties"

    def __post_init__(self):
        self.mass = Float(self.mass, config.float_precision)
        self.spin = Float(self.spin, config.float_precision)
        self.charge = Float(self.charge, config.float_precision)

        if self.mass < 0:
            raise LawOfConservationOfEnergy(f"Negative mass contradicts the general theory of relativity.")
        
        if abs(self.spin) > self._max_allowed_spin:
            raise CosmicCensorshipHypothesis(f"The amount of spin stated exceeds '{self._max_allowed_spin}' (meters) and therefore violates the cosmic censorship hypothesis.")
        
        if abs(self.charge) > self._max_allowed_charge:
            raise CosmicCensorshipHypothesis(f"The amount of charge stated exceeds '{self._max_allowed_charge}' (coloumb) and therefore violates the cosmic censorship hypothesis.")

        if   not self.spins and not self.charged:
            self.metric = SchwarzschildMetric
        elif not self.spins and     self.charged:
            self.metric = ReissnerNordströmMetric
        elif     self.spins and not self.charged:
            self.metric = KerrMetric
        elif     self.spins and     self.charged:
            self.metric = KerrNewmanMetric

    def _calc_property(self, eq: Equality, unknown: Symbol, overwrite: dict[Symbol, float] = {}) -> float:

        getters = {
            r_minus: lambda: self.innerHorizon,
            r_plus:  lambda: self.outerHorizon,
            R:       lambda: self.radius,
            M:       lambda: self.mass,
            M_irr:   lambda: self.irreducible_mass, 
            a:       lambda: self.spin,
            Q:       lambda: self.charge,
            A:       lambda: self.horizon_area,
            κ:       lambda: self.surface_gravity
        }

        getters.update({k: (lambda v=v: v) for k, v in overwrite.items()})

        solved = solve(eq, unknown)
        if not solved:
            raise FaultyImplementation(f"Cannot solve equation for {unknown}: {eq}")

        needed_symbols = solved[0].free_symbols

        values = {}
        for symbol, getter in getters.items():
            if symbol in needed_symbols and symbol != unknown:
                try:
                    values[symbol] = getter()
                except RecursionError:
                    values[symbol] = None

        return calculate(eq=eq, values=values, unknown=unknown, mode="single")


    def advance_time(self, timespan: timedelta, /, warn_on_evaporation: bool = False) -> None:
        """Reevaluates the properties of the black hole as if `timespan` time had passed.<br>
        This will reduce it's mass due to hawking radiation.
        """
        seconds = timespan.total_seconds()

        # Hawking Radiation
        if seconds > self.evaporation_time:
            target_time = 0
            if warn_on_evaporation:
                warnings.warn(f"The black hole evaporated in the process of advancing {seconds} seconds (after {(100 * self.evaporation_time / seconds):.2f}%).")
        else:
            target_time = self.evaporation_time - seconds

        self.mass = self._calc_property(self.metric.evaporation_time, M, {τ: target_time})

        # Calculations for spin and charge missing

    def penrose_process(self, delta_J: float, /, warn_on_extremal: bool = True) -> None:
        """Applies a Penrose-like rotational energy extraction by reducing the spin angular momentum J.

        Parameters
        ----------
        delta_J : float
            The amount of angular momentum to remove (in SI units, kg·m²/s).
        warn_on_extremal : bool, optional
            Warn if process would push the black hole below Schwarzschild limit (a < 0).
        """

        J_initial = self.angular_momentum

        J_final = J_initial - delta_J
        if J_final < 0:
            if warn_on_extremal:
                warnings.warn("Penrose process would overshoot: J < 0 — limiting to Schwarzschild.")
            J_final = 0.0

        self.spin = self._calc_property(formulas.spin_momentum, a, overwrite={J: J_final})
        self.mass = self._calc_property(Equality(M, sqrt(M_irr**2 + (J_final**2 * c**2) / (4 * G**2 * M_irr**2))), M)


    def feed(self, mass: float, /) -> None:
        """Increases the black holes mass the given amount."""
        self.mass += mass
    
    @property
    def spins(self) -> bool:
        "Whether the black hole spins"
        return not self.spin == 0
        
    @property
    def charged(self) -> bool:
        "Whether the black hole has charge"
        return not self.charge == 0
    
    @property
    def _max_allowed_spin(self) -> float:
        return (G * self.mass) / c**2
    
    @property
    def _max_allowed_charge(self) -> float:
        return sqrt(4 * π * ε_0 * G) * self.mass
    
    @property
    def angular_momentum(self) -> float:
        "Angular momentum of the black hole"
        return self._calc_property(formulas.spin_momentum, J)
    
    @property
    def dimless_spin(self) -> float:
        ""
        return self._calc_property(formulas.dimensionless_spin, a_star)
    
    @property
    def horizons(self) -> tuple[float, float | None]:

        return (
            self._calc_property(self.metric.r_plus, r_plus),
            self._calc_property(self.metric.r_minus, r_minus) if self.metric.r_minus is not None else None
        )
    
    @property
    def innerHorizon(self) -> float | None:
        "Radius of the black holes inner event horizon"
        return self.horizons[1]
    
    @property
    def outerHorizon(self) -> float:
        "Radius of the black holes outer event horizon"
        return self.horizons[0]
    
    @property
    def radius(self) -> float:
        "Radius of the black hole given by the outermost event horizon"
        return self.outerHorizon
    
    @property
    def horizon_area(self) -> float:
        """
        Area of the black hole's outermost event horizon<br>
        This area can be larger than the surface area of a sphere with the black hole's radius.
        """
        return self._calc_property(self.metric.horizon_area, A)

    @property
    def volume(self) -> float:
        """Volume of the black hole<br>
        This volume can be larger than the volume of a sphere with the black hole's radius.
        """
        if not self.metric == SchwarzschildMetric:
            warnings.warn("Volume calculation for black holes that aren't of the Schwarzschild metric is only approximated.")
        return (self.radius**3 * π * 4/3)

    @property
    def density(self) -> float:
        "Density of the black hole"
        return self._calc_property(Equality(ρ, M / V), ρ, {V: self.volume})
    
    @property
    def surface_gravity(self) -> float:
        "Surface gravity of the black hole"
        return self._calc_property(self.metric.surface_gravity, κ)
    
    @property
    def temperature(self) -> float:
        "Hawking temperature of the black hole"
        return self._calc_property(self.metric.hawking_temperature, T_H)
    
    @property
    def irreducible_mass(self) -> float:
        "Gravitational mass of the black hole that isn't a side effect of spin or charge"
        # raise FaultyImplementation("Can't be calculated because float precision")
        return self._calc_property(formulas.irreducable_mass, M_irr)
    
    @property
    def reducable_mass(self) -> float:
        "Gravitational mass of the black hole that is a side effect of spin or charge and thus can be extracted by a Penrose process or magnetic extraction"
        return Float(self.mass, precision=config.float_precision) - self.irreducible_mass
    
    @property
    def hawking_power(self) -> float:
        "Power of the black hole's Hawking radiation"
        return self._calc_property(self.metric.hawking_power, P)
    
    @property
    def evaporation_time(self) -> float:
        "Amount of time until the black hole will have completely evaporated"
        return self._calc_property(self.metric.evaporation_time, τ)

    def __getattribute__(self, name):
        try:
            value = super().__getattribute__(name)

        except Exception as e:
            msg = str(e)
            if match := regex.search(r"cannot sympify object of type <class 'ellipsis'>", msg):
                raise NotImplementedError(
                    f"Calculation of '{name}' has not yet been implemented for {self.metric} black holes.\n" + 
                    f"It is not definitely stated, but this is most certainly the case, because the dependencies of the parameters are non-trivial "
                    f"and thus, a calculation process would be very complex."
                )
            raise e
        
        return value
        
    def __repr__(self):
        return f"BlackHole(M={self.mass}, Q={self.charge}, a={self.spin})"