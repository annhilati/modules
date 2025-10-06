from sympy import Symbol, Float, NumberSymbol, pi
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

c:      Float = Float(299792458)            # meter / second                   # exact
G:      Float = Float('6.67430e-11')        # meter^3 / (kilogram second^2)    # not exact
ℏ:      Float = Float('1.054571817e-34')    # joule seconds                    # exact
k_B:    Float = Float('1.380649e-23')       # joule / kelvin                   # exact
ε_0:    Float = Float('8.8541878188e-12')   # ampere seconds / volt meter      # not exact

sunmass:        Float = Float('1.989e30',  precision=config.float_precision)             # kilogram
earthmass:      Float = Float('5.969e24',  precision=config.float_precision)             # kilogram
moonmass:       Float = Float('7.346e11',  precision=config.float_precision)             # kilogram
sagitariusmass: Float = Float('4_300_000', precision=config.float_precision) * sunmass  # kilogram
ton618mass:     Float = Float('6.600e11' , precision=config.float_precision) * sunmass  # kilogram