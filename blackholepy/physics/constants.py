# __all__ = ["c", "G", "ℏ",
#            "sunmass", "earthmass", "moonmass"]

from sympy import Expr
from sympy.physics.units import meter, second, kilogram, joule, kelvin

c: Expr = 299792458 * (meter / second)
G: Expr = 6.67430 * 10**-11 * (meter**3 / (kilogram * second**2))
ℏ: Expr = 6.62607015 * 10**-34 * joule * second
k_B: Expr = 1.380649 * 10**-23 * (joule / kelvin)

sunmass: Expr = 1.989 * 10**30 * kilogram
earthmass: Expr = 5.969 * 10**24 * kilogram
moonmass: Expr = 7.346 * 10**22 * kilogram

