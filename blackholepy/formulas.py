from sympy import Equality, sqrt, pi
from blackholepy.physics.constants import *
from blackholepy.symbols import *

spin_momentum: Equality = Equality(a, (J / M))

spin_parameter: Equality = Equality(a_param, (c * J) / (G * M**2))

density: Equality = Equality(ρ, M / ( (4/3) * pi * R**3 ))
"""
ρ (M * L^-3): density
M (M): mass
R (L): radius
"""

kerrNewmanRadius: tuple[Equality, Equality] = (
    Equality(R, ((G * M) / c**2) + (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / c**4) - a**2))),
    Equality(R, ((G * M) / c**2) - (sqrt(((G * M) / c**2)**2 - ((G * Q**2) / c**4) - a**2)))
)

oberflächenSchwerebeschleunigung: Equality = Equality(κ, (c**4 * (R - R2)) / (2 * G * (R**2 + a**2)))

hawkingTemperature: Equality = Equality(T_H, (ℏ * κ) / (2 * pi * k_B * c))