from dataclasses import dataclass

from sympy import Expr, solve, pi

import blackholepy.formulas as formulas
from blackholepy.formulas import calculate
from blackholepy.symbols import *
from blackholepy.constants import *
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

    :param M: Mass
    :type M: kilogram as float
    :param Q: Charge
    :type Q: coloumb as float
    :param a: Spin
    :type a: meter as float
    :raises CosmicCensorshipHypothesis: If the spin is so high that the horizons become imaginary
    """
        
    mass:   float
    charge: float = 0
    spin:   float = 0

    def __post_init__(self):
        if self.spin > (max_spin := (G * self.mass) / c**2):
            raise CosmicCensorshipHypothesis(f"The amount of spin stated exceeds '{max_spin}' (meters) and therefore violates the cosmic censorship hypothesis")
        
    def __repr__(self):
        return f"BlackHole(M={self.mass}, Q={self.charge}, a={self.spin})"

    @property
    def horizons(self) -> tuple[float]:
        out = []
        for eq in formulas.kerrNewmanRadius:
            out.append(calculate(eq, {M: self.mass, Q: self.charge, a: self.spin}, R)[0])

        if not self.spins:
            out[1] = out[0]
        return tuple(out)
    
    @property
    def spins(self) -> bool:
        "Returns whether the black hole spins"
        return not self.spin == 0
        
    @property
    def charged(self) -> bool:
        "Returns whether the black hole has charge"
        return not self.charge == 0
    
    @property
    def innerHorizon(self) -> float:
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
        return (self.radius ** 3 * pi * 4/3)

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
        return calculate(formulas.surface_gravity, {R: self.outerHorizon, R2: self.innerHorizon, a: self.spin}, κ)[0]
    
    @property
    def temperature(self) -> float:
        return calculate(formulas.hawkingTemperature, {κ: self.surface_gravity}, T_H)[0]