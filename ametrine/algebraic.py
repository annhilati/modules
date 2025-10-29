from __future__ import annotations

from dataclasses import dataclass, field
from ametrine.rational import rational

from math import gcd, isqrt

@dataclass
class algebraic:
    coefficients:   list[int]
    root_index:     int         = 0

    def __post_init__(self):
        if any([not isinstance(coefficient, int) for coefficient in self.coefficients]):
            raise TypeError
        
        if len(self.coefficients) < 2:
            raise ValueError

    def __repr__(self) -> str:
        if self.degree == 2:
            a, b, c = self.coefficients[2], self.coefficients[1], self.coefficients[0]
            disc = b**2 - 4*a*c
            sign = 1 if self.root_index == 0 else -1

            # Bruch + Wurzel vereinfachen
            k, r, denom = self.simplify_sqrt_div(disc, 2*a)
            if sign < 0:
                k = -k
            return f"{str(k) + "*" if k != 1 else ""}{"sqrt(" + r + ")" if r != 1 else "1"}{"/" + str(denom) if denom != 1 else ""}"
        return f"<'{self.root_index + 1}.' solution of the polynome '0 = {' + '.join(f'{c}x^{i}' for i, c in enumerate(self.coefficients))}'>"

    @staticmethod
    def simplify_sqrt_div(n, denom):
        """Vereinfacht sqrt(n)/denom zu k*sqrt(r)/d"""
        k = 1
        for i in range(2, isqrt(n)+1):
            while n % (i*i) == 0:
                n //= i*i
                k *= i
        g = gcd(k, denom)
        k //= g
        denom //= g
        return k, n, denom
      
    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

@dataclass
class root(algebraic):
    radicand:       rational
    exponent:       rational
    coefficients:   list[int]   = field(init=False)
    root_index:     int         = field(init=False, default=0)

    def __post_init__(self):
        self.coefficients, self.root_index = algebraic_from_root(self.radicand, self.exponent)

    def __repr__(self) -> str:
        return super().__repr__()

    def __mul__(self, other) -> root:
        if isinstance(other, root) and other.exponent == self.exponent:
            return root(
                radicand=self.radicand * other.radicand,
                exponent=self.exponent
            )
        
    def __truediv__(self, other) -> root:
        if isinstance(other, root) and other.exponent == self.exponent:
            return root(
                radicand=self.radicand / other.radicand,
                exponent=self.exponent
            )


def algebraic_from_root(r: rational | algebraic | int, e: int | rational):

    if isinstance(e, rational):
        # e = p/q
        p, q = e.numerator, e.denominator
        return algebraic_from_root(algebraic_from_root(r, p), rational(1, q))

    if not isinstance(e, int):
        raise TypeError("Exponent muss int oder Rational sein")
    
    root_index = 0

    if isinstance(r, int):
        r = rational(r, 1)

    # r ist Rational
    if isinstance(r, rational):
        n, d = r.numerator, r.denominator
        coeffs = [-n]
        coeffs += [0]*(e-1)
        coeffs.append(d)
        # Polynom: d*x^e - n = 0

    # r ist Algebraic
    if isinstance(r, algebraic):
        # ersetze x durch x^e im Polynom von r
        coeffs = []
        for i, c in enumerate(r.coefficients):
            coeffs += [0]*(e*i - len(coeffs)) + [c]
            root_index = r.root_index

    return coeffs, root_index