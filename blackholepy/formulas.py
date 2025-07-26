from sympy import Equality, sqrt, pi, solve, Symbol, Expr
from blackholepy.constants import *
from blackholepy.symbols import *

spin_momentum: Equality = Equality(a, (J / M))

spin_parameter: Equality = Equality(a_param, (c * J) / (G * M**2))

density: Equality = Equality(ρ, M / ( (4/3) * pi * R**3 ))
"""
:param ρ: Density
:param M: Mass
:param R: Radius
"""

kerrNewmanRadius: tuple[Equality, Equality] = (
    Equality(R, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - a**2))),
    Equality(R, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - a**2)))
)

surface_gravity = Equality(κ, (c**4 * (R - R2)) / (2 * G * (R**2 + a**2)))

hawkingTemperature: Equality = Equality(T_H, (ℏ * κ) / (2 * pi * k_B * c))

def calculate(
    eq: Equality,
    values: dict[Symbol, float],
    symbol: Symbol,
    precision: int = 50
) -> list[Expr | float]:
    
    formulas: list[Expr | float] = solve(eq, symbol)
    solutions = [
        formula.subs(values).evalf(n=precision)
        for formula in formulas
    ]
    return solutions