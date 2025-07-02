from sympy import Equality, sqrt, pi
from sympy.physics.units import meter, second
from .physics.constants import *
from .symbols import *

spin_momentum: Equality = Equality(a, (J / M) / (meter**2 / second))
"""
a (N): spin
J (M * L^2 * T^-1): angular momentum
M (M): mass
"""

density: Equality = Equality(ρ, M / ( (4/3) * pi * R**3 ))
"""
ρ (M * L^-3): density
M (M): mass
R (L): radius
"""

kerrNewmanRadius = [None,
                         Equality(R, ((G * M) / c**2) + (1 / c**2 * sqrt(((G * M)**2) - (G * Q**2) - (a**2 * c**2)))),
                         Equality(R, ((G * M) / c**2) - (1 / c**2 * sqrt(((G * M)**2) - (G * Q**2) - (a**2 * c**2))))]

oberflächenSchwerebeschleunigung = Equality(κ, (c**4 * (R - R2)) / (2 * G * (R**2 + a**2)))

hawkingTemperature = Equality(T_H, (ℏ * κ) / (2 * pi * k_B * c))