from .formulas import *
from .symbols import *
from .exceptions import *
from .physics.utils import dimensions
from sympy import Number, Expr, Mul, solve
from sympy.physics.units import mass, charge, length, coulomb, meter, second
from sympy.assumptions import assuming, Q as qq


class BlackHole():
    
    def __init__(self, M: Expr, Q: Expr = 0 * coulomb, a: Expr | float = 0):
        
        if dimensions(M) == mass:
            self.mass = M
        else:
            raise DimensionError(f"{M} does not have {mass} dimension")
        
        if dimensions(Q) == charge:
            self.charge = Q
        elif isinstance(Q, Number):
            self.charge = Mul(0, coulomb, evaluate=False)
        else:
            raise DimensionError(f"{Q} does not have {charge} dimension")
        
        if isinstance(a, float) or isinstance(a, int):
            self.spin = Number(a)
        elif dimensions(a) == length:
            self.spin = (a / meter)
        elif isinstance(a, Number):
            self.spin = a
        else:
            raise DimensionError(f"{a} has to be float or Expr type")
        
    def __repr__(self):
        return f"BlackHole(M={self.mass}, Q={self.charge}, a={self.spin})"

    @property
    def spins(self) -> bool:
        "Returns whether the black hole spins"
        if float(self.spin) == 0:
            return False
        else:
            return True
        
    @property
    def charged(self) -> bool:
        "Returns whether the black hole has charge"
        if float(self.charge) == 0:
            return False
        else:
            return True
        
    @property
    def innerHorizon(self) -> Expr:
        "Returns the radius of the black holes inner event horizon"
        eq = kerrNewmanRadius[2]

        eq = eq.simplify()
        eq = eq.subs({M: self.mass, Q: self.charge, a: self.spin})
        
        solutions: list[Expr] = solve(eq, R)
        solution = solutions[0].subs({meter: 1, second: 1}).evalf() * meter
        return solution
    
    @property
    def outerHorizon(self) -> Expr:
        "Returns the radius of the black holes outer event horizon"

        eq = kerrNewmanRadius[1]

        with assuming(qq.positive(G), qq.positive(M), qq.positive(c), qq.real(Q), qq.real(a)):
            eq = eq.simplify()
            eq = eq.subs({M: self.mass, Q: self.charge, a: self.spin})
            
            solutions: list[Expr] = solve(eq, R)
            solution = solutions[0].subs({meter: 1, second: 1}).evalf() * meter
        return solution

    @property
    def radius(self) -> Expr:
        "Returns the black holes radius"
        return self.outerHorizon

    @property
    def volume(self) -> Expr:
        return (self.radius ** 3 * pi * 4/3).evalf()

    @property
    def density(self) -> Expr:
        "Returns the black holes density"
        eq = density
        eq = eq.simplify()
        eq = eq.subs({M: self.mass, R: self.radius})
        solutions: list[Expr] = solve(eq, ρ)
        return solutions[0].simplify()
    
    @property
    def angularMomentum(self) -> Expr:
        "Returns the black holes angular momentum resulting in the specific angular momentum"
        eq = spin_momentum
        eq = eq.subs({a: self.spin, M: self.mass})
        solutions: list[Expr] = solve(eq, J)
        return solutions[0].simplify()