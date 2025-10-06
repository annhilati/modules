from sympy import Equality, sqrt, solve, Symbol, Expr
from dataclasses import dataclass
from typing import Literal

from blackholepy.symbols import *
import blackholepy.config as config

@dataclass
class BlackHoleMetric():
    """Class representing a set of formulas rigarding properties of black holes, result from a solution to the Einstein field equations and are true under certain circumstances."""
    
    name:                str
    r_plus:              Equality
    r_minus:             Equality | None
    surface_gravity:     Equality
    horizon_area:        Equality
    hawking_temperature: Equality
    hawking_power:       Equality
    evaporation_time:    Equality

    def __repr__(self):
        return f"<BlackHoleMetric '{self.name}'>"
    
    def __str__(self):
        return self.name

SchwarzschildMetric = BlackHoleMetric(
    name                    = "Schwarzschild metric",
    r_plus                  = Equality(r_plus, (2 * G * M) / c**2),
    r_minus                 = None,
    surface_gravity         = Equality(κ, c**4 / (4 * G * M)),
    horizon_area            = Equality(A, 4 * pi * r_plus**2),
    hawking_temperature     = Equality(T_H, (ℏ * κ) / (2 * pi * k_B * c)),
    hawking_power           = Equality(P, (ℏ * c**6) / (15360 * pi * G**2 * M **2)),
    evaporation_time        = Equality(τ, (5120 * pi * G**2 * M**3) / (ℏ * c**4))
)

ReissnerNordströmMetric = BlackHoleMetric(
    name                    = "Reissner-Nordström metric",
    r_plus                  = Equality(r_plus, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4))))),
    r_minus                 = Equality(r_minus, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4))))),
    surface_gravity         = Equality(κ, (c**4 / (4 * G * M)) * (1 - ((Q**2 * G) / (4 * pi * ε_0 * c**4 * M**2)))),
    horizon_area            = Equality(A, 4 * pi * r_plus**2),
    hawking_temperature     = Equality(T_H, ((ℏ * c**3) / (2 * pi * k_B * G * M)) * sqrt(1 - ((Q**2 * G) / (4 * pi * ε_0 * c**4 * M**2)))),
    hawking_power           = ...,
    evaporation_time        = ...
)

KerrMetric = BlackHoleMetric(
    name                    = "Kerr metric",
    r_plus                  = Equality(r_plus, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - a**2))),
    r_minus                 = Equality(r_minus, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - a**2))),
    surface_gravity         = Equality(κ, c**2 * sqrt(((G * M) / c**2)**2 - a**2) / (r_plus**2 + a**2)),
    horizon_area            = Equality(A, 4 * pi * (r_plus**2 + a**2)),
    hawking_temperature     = Equality(T_H, ((ℏ * c**3) / (2 * pi * k_B * G * M)) * ((sqrt(1 - a_star**2)) / (1 + sqrt(1 - a_star**2)))),
    hawking_power           = ...,
    evaporation_time        = ...
)

KerrNewmanMetric = BlackHoleMetric(
    name                    = "Kerr-Newman metric",
    r_plus                  = Equality(r_plus, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - (a**2 / c**2)))),
    r_minus                 = Equality(r_minus, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / (4 * pi * ε_0 * c**4)) - (a**2 / c**2)))),
    surface_gravity         = Equality(κ, (c**4 * (r_plus - r_minus)) / (2 * G * (r_plus**2 + a**2))),
    horizon_area            = Equality(A, 4 * pi * (r_plus**2 + a**2)),
    hawking_temperature     = Equality(T_H, ((ℏ * c**3) / (2 * pi * k_B * G * M)) * (sqrt(M**2 - a**2 + ((Q**2 * G) / (4 * pi * ε_0 * c**4))) / ((M + sqrt(M**2 - a**2 + ((Q**2 * G) / (4 * pi * ε_0 * c**4))))**2 + a**2))),
    hawking_power           = ...,
    evaporation_time        = ...
)

spin_momentum: Equality = Equality(a, (J / M))

dimensionless_spin: Equality = Equality(a_star, a / ((G * M) / c**2))

irreducable_mass: Equality = Equality(M_irr, sqrt((c**4 * A) / (16 * pi * G**2)))

entropy: Equality = Equality(S, (k_B * c**3 * A) / (4 * G * ℏ))

def calculate(
    eq: Equality,
    values: dict[Symbol, float],
    unknown: Symbol,
    mode: Literal["single", "set"] = "single",
    precision: int = config.float_precision
) -> Expr | float | set[Expr | float]:
    
    formulas: list[Expr] = solve(eq, unknown)
    solutions = [
        formula.evalf(
            n=precision,
            maxn=300,
            subs={
                    symbol: value
                    for symbol, value in values.items()
                    if value is not None
                }
        )
        for formula in formulas
    ]
    if mode == "single":
        return solutions[0]
    return set(solutions)