from dataclasses import dataclass, field

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

    :param mass: Mass
    :type mass: kilogram as float
    :param charge: Charge
    :type charge: coloumb as float
    :param spin: Spin
    :type spin: meter as float
    :raises CosmicCensorshipHypothesis: If the spin is so high that the horizons become imaginary
    """
        
    mass:   float
    charge: float = 0
    spin:   float = 0
    metric: BlackHoleMetric = field(init=False)

    def __post_init__(self):
        if self.spin > (max_spin := (G * self.mass) / c**2):
            raise CosmicCensorshipHypothesis(f"The amount of spin stated exceeds '{max_spin}' (meters) and therefore violates the cosmic censorship hypothesis")
        
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
            outer = calculate(self.metric.r_plus, map, R)[0]
        if self.metric.r_minus is not None:
            inner = calculate(self.metric.r_minus, map, R)[0]
        return (outer, inner)
    
    @property
    def spins(self) -> bool:
        "Returns whether the black hole spins"
        return not self.spin == 0
        
    @property
    def charged(self) -> bool:
        "Returns whether the black hole has charge"
        return not self.charge == 0
    
    @property
    def innerHorizon(self) -> float | None:
        "Returns the radius of the black holes inner event horizon"
        return self.horizons[1]
    
    @property
    def outerHorizon(self) -> float:
        "Returns the radius of the black holes outer event horizon"
        return self.horizons[0]
    
    @property
    def radius(self) -> float:
        "Returns the black holes radius"
        return self.outerHorizon

    @property
    def volume(self) -> float:
        return (self.radius ** 3 * π * 4/3)

    @property
    def density(self) -> float:
        "Returns the black holes density"
        return calculate(formulas.density, {M: self.mass, R: self.radius}, ρ)[0]
    
    @property
    def angularMomentum(self) -> float:
        "Returns the black holes angular momentum resulting in the specific angular momentum"
        return calculate(formulas.spin_momentum, {a: self.spin, M: self.mass}, J)
    
    @property
    def surface_gravity(self) -> float:
        map = {M: self.mass, R: self.outerHorizon, R2: self.innerHorizon, a: self.spin}
        return calculate(self.metric.surface_gravity, {symbol: value for symbol, value in map.items() if value is not None}, κ)[0]
    
    @property
    def temperature(self) -> float:
        map = {κ: self.surface_gravity}
        return calculate(formulas.hawkingTemperature, {symbol: value for symbol, value in map.items() if value is not None}, T_H)[0]