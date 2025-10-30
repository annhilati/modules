from typing import TypeAlias, Literal

PolynomialCoefficients: TypeAlias = list[int]
"""List of integers.

A list of polynomial coefficients `[1, 0, -3, 0, 0, 2]` is equivalent to a polynomial *0 = 1 + 0x -3x^2 + 0x^3 + 0x^4 + 2x^5*"""

Digit: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]