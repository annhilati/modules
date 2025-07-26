from sympy import Equality, sqrt, pi, solve, Symbol, Expr
from dataclasses import dataclass

from blackholepy.symbols import *
import blackholepy.config as config

@dataclass
class BlackHoleMetric():
    
    name:            str
    r_plus:          Equality
    r_minus:         Equality | None
    surface_gravity: Equality

    def __repr__(self):
        return f"<BlackHoleMetric '{self.name}'>"

SchwarzschildMetric = BlackHoleMetric(
    name            = "Schwarzschild metric",
    r_plus          = Equality(R, (2 * G * M) / c**2),
    r_minus         = None,
    surface_gravity = Equality(κ, c**4 / (4 * G * M))
)

ReissnerNordströmMetric = BlackHoleMetric(
    name            = "Reissner-Nordström metric",
    r_plus          = Equality(R, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4))))),
    r_minus         = Equality(R, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4))))),
    surface_gravity = Equality(κ, (c**4 * (R - R2)) / (2 * G * (R**2 + a**2)))
)

KerrMetric = BlackHoleMetric(
    name            = "Kerr metric",
    r_plus          = Equality(R, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - a**2))),
    r_minus         = Equality(R, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - a**2))),
    surface_gravity = Equality(κ, (c**4 * (R - R2)) / (2 * G * (R**2 + a**2)))
)

KerrNewmanMetric = BlackHoleMetric(
    name            = "Kerr-Newman metric",
    r_plus          = Equality(R, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - a**2))),
    r_minus         = Equality(R, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - a**2))),
    surface_gravity = Equality(κ, (c**4 * (R - R2)) / (2 * G * (R**2 + a**2)))
)

spin_momentum: Equality = Equality(a, (J / M))

spin_parameter: Equality = Equality(a_param, (c * J) / (G * M**2))

density: Equality = Equality(ρ, M / ( (4/3) * pi * R**3 ))
"""
:param ρ: Density
:param M: Mass
:param R: Radius
"""

hawkingTemperature: Equality = Equality(T_H, (ℏ * κ) / (2 * pi * k_B * c))


def calculate(
    eq: Equality,
    values: dict[Symbol, float],
    symbol: Symbol,
    precision: int = config.float_precision
) -> list[Expr | float]:
    
    formulas: list[Expr | float] = solve(eq, symbol)
    solutions = [
        formula.subs(values).evalf(n=precision)
        for formula in formulas
    ]
    return solutions