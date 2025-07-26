from sympy import Equality, sqrt, solve, Symbol, Expr
from dataclasses import dataclass

from blackholepy.symbols import *
import blackholepy.config as config

@dataclass
class BlackHoleMetric():
    
    name:            str
    r_plus:          Equality
    r_minus:         Equality | None
    surface_gravity: Equality
    horizon_area:    Equality

    def __repr__(self):
        return f"<BlackHoleMetric '{self.name}'>"

SchwarzschildMetric = BlackHoleMetric(
    name            = "Schwarzschild metric",
    r_plus          = Equality(r_plus, (2 * G * M) / c**2),
    r_minus         = None,
    surface_gravity = Equality(κ, c**4 / (4 * G * M)),
    horizon_area    = Equality(A, 4 * pi * r_plus**2)
)

ReissnerNordströmMetric = BlackHoleMetric(
    name            = "Reissner-Nordström metric",
    r_plus          = Equality(r_plus, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4))))),
    r_minus         = Equality(r_minus, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4))))),
    surface_gravity = Equality(κ, (c**4 / (4 * G * M)) * (1 - ((Q**2 * G) / (4 * pi * ε_0 * c**4 * M**2)))),
    horizon_area    = Equality(A, 4 * pi * r_plus**2)
)

KerrMetric = BlackHoleMetric(
    name            = "Kerr metric",
    r_plus          = Equality(r_plus, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - a**2))),
    r_minus         = Equality(r_minus, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - a**2))),
    surface_gravity = Equality(κ, (c**4 * sqrt(G**2 * M**2 - a**2 * c**2)) / (2 * G * M * (((G * M) / c**2 + sqrt(((G * M) / c**2)**2 - (a**2 / c**2)))**2 + a**2))),
    horizon_area    = Equality(A, 4 * pi * (r_plus**2 + a**2))
)

KerrNewmanMetric = BlackHoleMetric(
    name            = "Kerr-Newman metric",
    r_plus          = Equality(r_plus, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - (a**2 / c**2)))),
    r_minus         = Equality(r_minus, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - (a**2 / c**2)))),
    surface_gravity = Equality(κ, (c**4 * (r_plus - r_minus)) / (2 * G * (r_plus**2 + a**2))),
    horizon_area    = Equality(A, 4 * pi * (r_plus**2 + a**2))
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

irreducable_mass: Equality = Equality(M_irr, sqrt((c**4 * A) / (16 * pi * G**2)))

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