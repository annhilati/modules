from sympy import Expr, solve, pi
from dataclasses import dataclass
import blackholepy.formulas as formulas
from blackholepy.symbols import *
from blackholepy.exceptions import *

@dataclass
class BlackHole():
    """Class representing a black hole.

    :param M: Mass
    :type M: kilogram as float
    :param Q: Charge
    :type Q: coloumb as float
    :param a: Spin
    :type a: meter as float
    """
        
    mass:   float
    charge: float = 0      
    spin:   float = 0
        
    def __repr__(self):
        return f"BlackHole(M={self.mass} kg, Q={self.charge} C, a={self.spin} m)"

    @property
    def spins(self) -> bool:
        "Returns whether the black hole spins"
        return self.spin == 0
        
    @property
    def charged(self) -> bool:
        "Returns whether the black hole has charge"
        return self.charge == 0
    
    @property
    def horizons(self) -> tuple[float]:
        out = []
        for eq in formulas.kerrNewmanRadius:
            eq = eq.subs({M: self.mass, Q: self.charge, a: self.spin})
            solutions = solve(eq, R)
            out.append(solutions[0])

        return tuple(out)
        
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
        eq = formulas.density
        eq = eq.simplify()
        eq = eq.subs({M: self.mass, R: self.radius})
        solutions = solve(eq, ρ)
        return solutions[0]
    
    @property
    def angularMomentum(self) -> float:
        "Returns the black holes angular momentum resulting in the specific angular momentum"
        eq = formulas.spin_momentum
        eq = eq.subs({a: self.spin, M: self.mass})
        solutions: list[Expr] = solve(eq, J)
        return solutions[0].simplify()