from sympy import Symbol, Rational, NumberSymbol, pi, symbols
from blackholepy import config

# These symbols shall no longer be used a variables for specific Quantities
A       = Symbol("A")
a       = Symbol("a")
a_star  = Symbol("a_star")
J       = Symbol("J")
M       = Symbol("M")
M_irr   = Symbol("M_irr")
P       = Symbol("P")
Q       = Symbol("Q")
R       = Symbol("R")
r_minus = Symbol("r_minus")
r_plus  = Symbol("r_plus")
S       = Symbol("S")
T_H     = Symbol("T_H")
V       = Symbol("V")
τ       = Symbol("τ")
ρ       = Symbol("ρ")
κ       = Symbol("κ")

π:      NumberSymbol = pi

c       = Rational(299792458)
G       = Rational('6.67430e-11')
ℏ       = Rational('1.054571817e-34')
k_B     = Rational('1.380649e-23')
ε_0     = Rational('8.8541878188e-12')

constants = {
    c:      Rational(299792458),
    G:      Rational('6.67430e-11'),
    ℏ:      Rational('1.054571817e-34'),
    k_B:    Rational('1.380649e-23'),
    ε_0:    Rational('8.8541878188e-12')
}

# c:      Float = Float(299792458)            # meter / second                   # exact
# G:      Float = Float('6.67430e-11')        # meter^3 / (kilogram second^2)    # not exact
# ℏ:      Float = Float('1.054571817e-34')    # joule seconds                    # exact
# k_B:    Float = Float('1.380649e-23')       # joule / kelvin                   # exact
# ε_0:    Float = Float('8.8541878188e-12')   # ampere seconds / volt meter      # not exact

sunmass:        Rational = Rational('1.989e30')             # kilogram
earthmass:      Rational = Rational('5.969e24')             # kilogram
moonmass:       Rational = Rational('7.346e11')             # kilogram
sagitariusmass: Rational = Rational('4_300_000') * sunmass  # kilogram
ton618mass:     Rational = Rational('6.600e11') * sunmass  # kilogram