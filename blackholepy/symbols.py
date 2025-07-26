from sympy import Symbol

M       = Symbol("mass",                real=True)
Q       = Symbol("charge",              real=True)
a       = Symbol("spin",                real=True)
a_param = Symbol("spin_star",           real=True)
R       = Symbol("radius")
R2      = Symbol("radius2")
ρ       = Symbol("density",             real=True)
J       = Symbol("angular-momentum")
κ       = Symbol("surface-gravity")
T_H     = Symbol("hawking-temperature", real=True, positive=True)


c:      float = 299792458                # meter / second
G:      float = 6.67430      * 10**-11   # meter^3 / (kilogram second^2)
ℏ:      float = 6.62607015   * 10**-34   # joule seconds
k_B:    float = 1.380649     * 10**-23   # joule / kelvin
ε_0:    float = 8.8541878188 * 10**-12   # ampere seconds / volt meter

sunmass:    float = 1.989 * 10**30 # kilogram
earthmass:  float = 5.969 * 10**24 # kilogram
moonmass:   float = 7.346 * 10**22 # kilogram
sagitariusmass: float = 4300000 * sunmass # kilogram
