from dataclasses import dataclass, field
import warnings

from sympy import sqrt

import blackholepy.formulas as formulas
from blackholepy.formulas import calculate, BlackHoleMetric, KerrMetric, KerrNewmanMetric, SchwarzschildMetric, ReissnerNordströmMetric
from blackholepy.symbols import *
from blackholepy.exceptions import *

# def spin_from_spin_param(spin_param: float, mass: float, /):
#     eq = formulas.spin_parameter
#     eq = eq.subs({M: mass, a_param: spin_param})
#     solutions = solve(eq, J)
#     j = solutions[0]
#     eq = formulas.spin_momentum
#     eq = eq.subs({M: mass, J: j})
#     solutions = solve(eq, a)
#     print(solutions[0])
#     return solutions[0]

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
    CosmicCensorshipHypothesis : If parameters exceed certain limits so that the horizons become imaginary

    """
        
    mass:   float
    charge: float           = 0
    spin:   float           = 0
    metric: BlackHoleMetric = field(init=False)

    def __post_init__(self):
        if abs(self.spin) > (max_spin := (G * self.mass) / c**2):
            raise CosmicCensorshipHypothesis(f"The amount of spin stated exceeds '{max_spin}' (meters) and therefore violates the cosmic censorship hypothesis")
        
        if abs(self.charge) > (max_charge := (sqrt(4 * π * ε_0 * G) * self.mass).evalf()):
            raise CosmicCensorshipHypothesis(f"The amount of charge stated exceeds '{max_charge}' (coloumb) and therefore violates the cosmic censorship hypothesis")
        
        if self.mass < 0:
            raise BlackHolePyError(f"Cannot have negative mass")

        if not self.spin and not self.charge:
            self.metric = SchwarzschildMetric
        elif not self.spin and self.charge:
            self.metric = ReissnerNordströmMetric
        elif self.spin and not self.charge:
            self.metric = KerrMetric
        elif self.spin and self.charge:
            self.metric = KerrNewmanMetric
        
    def __repr__(self):
        return f"BlackHole(M={self.mass}, Q={self.charge}, a={self.spin})"    

    @property
    def horizons(self) -> tuple[float, float | None]:

        outer = None
        inner = None
        map = {
            M: self.mass,
            Q: self.charge,
            a: self.spin
        }

        if self.metric.r_plus is not None:            
            outer = calculate(self.metric.r_plus, map, r_plus)[0]
        if self.metric.r_minus is not None:
            inner = calculate(self.metric.r_minus, map, r_minus)[0]
        return (outer, inner)
    
    @property
    def spins(self) -> bool:
        "Whether the black hole spins"
        return not self.spin == 0
        
    @property
    def charged(self) -> bool:
        "Whether the black hole has charge"
        return not self.charge == 0
    
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
        return calculate(self.metric.horizon_area, {r_plus: self.outerHorizon, a: self.spin}, A)[0]

    @property
    def volume(self) -> float:
        "Volume of the black hole"
        if not self.metric == SchwarzschildMetric:
            warnings.warn("Volume calculation for black holes that aren't of the Schwarzschild metric is only approximated.")
        return (self.radius**3 * π * 4/3)

    @property
    def density(self) -> float:
        "Density of the black hole"
        return Float(self.mass) / Float(self.volume)
    
    @property
    def angular_momentum(self) -> float:
        "Angular momentum of the black hole"
        return calculate(formulas.spin_momentum, {a: self.spin, M: self.mass}, J)
    
    @property
    def surface_gravity(self) -> float:
        "Surface gravity of the black hole"
        return calculate(self.metric.surface_gravity, {M: self.mass, r_plus: self.outerHorizon, r_minus: self.innerHorizon, a: self.spin, Q: self.charge}, κ)[0]
    
    @property
    def temperature(self) -> float:
        "Hawking temperature of the black hole"
        return calculate(formulas.hawkingTemperature, {κ: self.surface_gravity}, T_H)[0]
    
    @property
    def irreducable_mass(self) -> float:
        "Gravitational mass of the black hole that can't be reduced through any process"
        return calculate(formulas.irreducable_mass, {A: self.horizon_area}, M_irr)[0]
    
    # @property
    # def reducable_mass(self) -> float:
    #     "Gravitational mass of the black hole that can be reduced through some process"
    #     return Float(self.mass) - Float(self.irreducable_mass)
    
    @property
    def hawking_power(self) -> float:
        return calculate(self.metric.hawking_power, {M: self.mass}, P)[0]
    
    @property
    def evaporation_time(self) -> float:
        return calculate(self.metric.evaporation_time, {M: self.mass}, t)[0]