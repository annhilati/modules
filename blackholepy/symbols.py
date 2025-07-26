from sympy import Symbol

M       = Symbol("mass")
Q       = Symbol("charge")
a       = Symbol("spin", real=True)
a_param = Symbol("spin_star", real=True)
R       = Symbol("radius")
R2      = Symbol("radius2")
ρ       = Symbol("density", real=True)
J       = Symbol("angular-momentum", real=True)
κ       = Symbol("surface-gravity", real=True)
T_H     = Symbol("hawking-temperature", real=True, positive=True)