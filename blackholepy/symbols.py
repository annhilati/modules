from sympy import Symbol, pi, Float

M       = Symbol("mass",                real=True)
M_irr   = Symbol("irreduacle-mass")
Q       = Symbol("charge",              real=True)
a       = Symbol("spin",                real=True)
a_param = Symbol("spin_star",           real=True)
R       = Symbol("radius")
r_plus  = Symbol("outer-horizon-radius")
r_minus = Symbol("inner-horizon-radius")
ρ       = Symbol("density",             real=True)
J       = Symbol("angular-momentum")
κ       = Symbol("surface-gravity")
T_H     = Symbol("hawking-temperature", real=True, positive=True)
A       = Symbol("horizon-area")
P       = Symbol("hawking-power")
t       = Symbol("time")

π:      ...   = pi

c:      Float = Float(299792458)            # meter / second                   # exact
G:      Float = Float('6.67430e-11')        # meter^3 / (kilogram second^2)    # not exact
ℏ:      Float = Float('1.054571817e-34')    # joule seconds                    # exact
k_B:    Float = Float('1.380649e-23')       # joule / kelvin                   # exact
ε_0:    Float = Float('8.8541878188e-12')   # ampere seconds / volt meter      # not exact

sunmass:    float = 1.989 * 10**30 # kilogram
earthmass:  float = 5.969 * 10**24 # kilogram
moonmass:   float = 7.346 * 10**22 # kilogram
sagitariusmass: float = 4300000 * sunmass # kilogram