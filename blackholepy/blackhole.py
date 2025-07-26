from sympy import Expr, solve
from blackholepy.formulas import *
from blackholepy.symbols import *
from blackholepy.exceptions import *
from blackholepy.physics.utils import dimensions

class BlackHole():
    
    def __init__(self, M: float, Q: float = 0, a: float = 0):
        
        self.mass = M
        self.charge = Q        
        self.spin = a
        
    def __repr__(self):
        return f"BlackHole(M={self.mass}, Q={self.charge}, a={self.spin})"

    @property
    def spins(self) -> bool:
        "Returns whether the black hole spins"
        return self.spin == 0
        
    @property
    def charged(self) -> bool:
        "Returns whether the black hole has charge"
        return self.charge == 0
        
    @property
    def innerHorizon(self) -> float:
        "Returns the radius of the black holes inner event horizon"
        eq: Equality = kerrNewmanRadius[1]

        eq = eq.subs({M: self.mass, Q: self.charge, a: self.spin})

        solutions = solve(eq, R)
        solution = solutions[0]
        return solution
    
    @property
    def outerHorizon(self) -> Expr:
        "Returns the radius of the black holes outer event horizon"
        eq: Equality = kerrNewmanRadius[0]

        eq = eq.subs({M: self.mass, Q: self.charge, a: self.spin})

        solutions = solve(eq, R)
        solution = solutions[0]
        return solution

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
        eq = density
        eq = eq.simplify()
        eq = eq.subs({M: self.mass, R: self.radius})
        solutions = solve(eq, ρ)
        return solutions[0]
    
    @property
    def angularMomentum(self) -> float:
        "Returns the black holes angular momentum resulting in the specific angular momentum"
        eq = spin_momentum
        eq = eq.subs({a: self.spin, M: self.mass})
        solutions: list[Expr] = solve(eq, J)
        return solutions[0].simplify()