from dataclasses import dataclass, field
from datetime import timedelta
import warnings
import re

from sympy import sqrt, Expr

from blackholepy import formulas, config
from blackholepy.formulas import calculate, BlackHoleMetric, KerrMetric, KerrNewmanMetric, SchwarzschildMetric, ReissnerNordströmMetric
from blackholepy.symbols import *
from blackholepy.exceptions import *

# Wrong result still
#
# def spin_from_spin_param(spin_param: float, mass: float, /):
    # value = calculate(formulas.spin_parameter, {M: mass, a_param: spin_param}, J)[0]
    # return calculate(formulas.spin_momentum, {M: mass, J: value}, a)[0]

@dataclass
class BlackHole():
    """Class representing a black hole.

    Parameters
    ----------
    mass : kilogram as float
    charge : coloumb as float
    spin : meter as float
        The Metric required here is the 'Kerr-parameter' *a*, messured in meters.<br>
        Not to be confused with the spin parameter *a*<sub>*</sub> (in [0, 1]) or the angular momentum *J* (kg m^2 / s).

    Raises
    ----------
    CosmicCensorshipHypothesis : If parameters exceed certain limits, so that event horizons become imaginary
    LawOfConservationOfEnergy : If parameters cause behavior that would destroy energy or create it out of nothing
    """
        
    mass:   float
    charge: float           = 0
    spin:   float           = 0
    metric: BlackHoleMetric = field(init=False)
    "Collection of formulas that descripe the black holes properties"

    def __post_init__(self):
        if self.mass < 0:
            raise LawOfConservationOfEnergy(f"Negative mass contradicts the general theory of relativity.")
        
        if abs(self.spin) > self._max_pos_spin:
            raise CosmicCensorshipHypothesis(f"The amount of spin stated exceeds '{self._max_pos_spin}' (meters) and therefore violates the cosmic censorship hypothesis.")
        
        if abs(self.charge) > self._max_pos_charge:
            raise CosmicCensorshipHypothesis(f"The amount of charge stated exceeds '{self._max_pos_charge}' (coloumb) and therefore violates the cosmic censorship hypothesis.")

        if not self.spin and not self.charge:
            self.metric = SchwarzschildMetric
        elif not self.spin and self.charge:
            self.metric = ReissnerNordströmMetric
        elif self.spin and not self.charge:
            self.metric = KerrMetric
        elif self.spin and self.charge:
            self.metric = KerrNewmanMetric

    def advance_time(self, timespan: timedelta | float, /, warn_on_evaporation: bool = False) -> None:
        """Reevaluates the properties of the black hole as if `timespan` time had passed.<br>
        This will reduce it's mass due to hawking radiation.
        """
        seconds = timespan.total_seconds() if isinstance(timespan, timedelta) else timespan

        if seconds > self.evaporation_time:
            target_time = 0
            if warn_on_evaporation:
                warnings.warn(f"The black hole has reached a mass of '0' in the process of warping {seconds} seconds (after {(100 * self.evaporation_time / seconds):.2f}%).")
        else:
            target_time = self.evaporation_time - seconds

        self.mass = calculate(self.metric.evaporation_time, {τ: target_time}, M)
    
    @property
    def spins(self) -> bool:
        "Whether the black hole spins"
        return not self.spin == 0
        
    @property
    def charged(self) -> bool:
        "Whether the black hole has charge"
        return not self.charge == 0
    
    @property
    def _max_pos_spin(self) -> float:
        return Expr((G * self.mass) / c**2).evalf()
    
    @property
    def _max_pos_charge(self) -> float:
        return Expr(sqrt(4 * π * ε_0 * G) * self.mass).evalf()
    
    @property
    def angular_momentum(self) -> float:
        "Angular momentum of the black hole"
        return calculate(formulas.spin_momentum, {a: self.spin, M: self.mass}, J)
    
    @property
    def dimless_spin(self) -> float:
        ""
        return calculate(formulas.dimensionless_spin, {a: self.spin, M: self.mass}, a_star)
    
    @property
    def horizons(self) -> tuple[float, float | None]:

        outer = None
        inner = None
        map = {
            M: self.mass,
            Q: self.charge,
            a: self.spin
        }
       
        outer = calculate(self.metric.r_plus, map, r_plus)
        if self.metric.r_minus is not None:
            inner = calculate(self.metric.r_minus, map, r_minus)
        return (outer, inner)
    
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
        return calculate(self.metric.horizon_area, {r_plus: self.outerHorizon, a: self.spin}, A)

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
        return Float(self.mass) / Float(self.volume)
    
    @property
    def surface_gravity(self) -> float:
        "Surface gravity of the black hole"
        return calculate(self.metric.surface_gravity, {M: self.mass, r_plus: self.outerHorizon, r_minus: self.innerHorizon, a: self.spin, Q: self.charge}, κ)
    
    @property
    def temperature(self) -> float:
        "Hawking temperature of the black hole"
        return calculate(self.metric.hawking_temperature, {κ: self.surface_gravity}, T_H)
    
    @property
    def irreducable_mass(self) -> float:
        "Gravitational mass of the black hole that can't be reduced through any process"
        return calculate(formulas.irreducable_mass, {A: self.horizon_area}, M_irr)
    
    # @property
    # def reducable_mass(self) -> float:
    #     "Gravitational mass of the black hole that can be reduced through some process"
    #     return Float(self.mass) - Float(self.irreducable_mass)
    
    @property
    def hawking_power(self) -> float:
        "Power of the black hole's Hawking radiation"
        return calculate(self.metric.hawking_power, {M: self.mass}, P)
    
    @property
    def evaporation_time(self) -> float:
        "Amount of time until the black hole will have completely evaporated"
        return calculate(self.metric.evaporation_time, {M: self.mass}, τ)

    def __getattribute__(self, name):
        try:
            value = super().__getattribute__(name)

        except Exception as e:
            msg = str(e)
            if match := re.search(r"cannot sympify object of type <class 'ellipsis'>", msg):
                raise NotImplementedError(f"'{name}' is not implemented for {self.metric} black holes yet")
            raise e
        
        return value
        
    def __repr__(self):
        return f"BlackHole(M={self.mass}, Q={self.charge}, a={self.spin})"