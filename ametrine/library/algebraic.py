from __future__ import annotations

from dataclasses import dataclass, field
from ametrine.library.rational import rational, rationalComprehendable
from ametrine.typing import PolynomialCoefficients

from math import gcd, isqrt

@dataclass
class algebraic:
    coefficients:   PolynomialCoefficients
    root_number:    int         = 0

    def __post_init__(self):
        if any([not isinstance(coefficient, int) for coefficient in self.coefficients]):
            raise TypeError
        
        if len(self.coefficients) < 2:
            raise ValueError

    def __repr__(self) -> str:
        if type(self.simplify()) in [int, rational]:
            return str(self.simplify())
        return f"<{self.root_number + 1}. solution of the polynomial '0 = {' + '.join(f'{c}x^{i}' for i, c in enumerate(self.coefficients))}'>"

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
    
    def simplify(self) -> algebraic | rational | int:
        """Gibt eine rationale Darstellung zurück, falls das Algebraic rational ist.
        Andernfalls wird self zurückgegeben.
        # TODO: Gibt teilweise negative Werte zurück, ergibt garkeinen Sinn. Teste: print(rational(5) ** rational(1, 2))
        """
        coeffs = self.coefficients
        root_index = self.root_number

        # Nur sinnvoll, wenn Wurzelindex 0 (erste Lösung)
        # und alle Koeffizienten ganze Zahlen oder Rationale sind
        if not all(hasattr(c, "__mul__") for c in coeffs):
            return self  # kein numerischer Typ

        # Rational Root Theorem anwenden
        a_n = coeffs[-1]
        a_0 = coeffs[0]

        # Potentielle rationale Kandidaten p/q mit p|a0, q|a_n
        ps = [i for i in range(-abs(a_0), abs(a_0) + 1) if i != 0 and a_0 % i == 0]
        qs = [i for i in range(1, abs(a_n) + 1) if a_n % i == 0]

        for p in ps:
            for q in qs:
                r = rational(p, q)
                val = sum(c * (r ** i) for i, c in enumerate(coeffs))
                if val == 0:
                    found = rational(p, q)
                    if root_index == 0:
                        return found.simplify()
                    else:
                        return rational(-found.numerator, found.denominator).simplify()


        return self  # keine rationale Lösung gefunden
    
    @property
    def polynomial_degree(self) -> int:
        return len(self.coefficients) - 1

    @property
    def is_rational(self) -> bool:
        return isinstance(self.simplify(), rational)

    @property
    def determinant(self) -> rational:
        ...

@dataclass
class root(algebraic):
    radicand:       rational
    index:          rational
    coefficients:   PolynomialCoefficients  = field(init=False)
    root_number:    int                     = field(init=False, default=0)

    # @property
    # def coefficients(self) -> list[int]:
    #     return algebraic_from_root(self.radicand, self.exponent)[0]
    
    # @property
    # def root_index(self) -> int:
    #     return algebraic_from_root(self.radicand, self.exponent)(1)

    def __post_init__(self):
        coefficients =  algebraic_from_root(self.radicand, self.index)[0]
        self.coefficients = coefficients
        for i, solution in enumerate(find_real_algebraic_roots(coefficients)):
            if self.radicand == solution:
                self.root_number = i

        if self.radicand < 0:
            raise ValueError

    def __repr__(self) -> str:
        return super().__repr__()
    
    @classmethod
    def comprehend(cls, obj: rootComprehendable) -> root:
        if isinstance(obj, rationalComprehendable):
            return cls(rational.comprehend(obj), 1)
        elif isinstance(obj, root):
            return cls(obj.radicand, obj.index)

    def __mul__(self, other) -> root:
        if isinstance(other, root) and other.index == self.index:
            return root(
                radicand=self.radicand * other.radicand,
                index=self.index
            )
        return super().__mul__()
    
    def __eq__(self, other):
        other = root.comprehend(other)
        return (
            self.radicand == other.radicand and self.index == other.index
            or
            self.simplify() == other.simplify()
        )

rootComprehendable = int | float | rational | root
        
def algebraic_from_root(radicand: rationalComprehendable, index: rationalComprehendable):
    """
    Bestimmt das Minimalpolynom und den Lösungsindex einer algebraischen Zahl x = radicand^(1/index).
    Annahme: kein Fehlerfall, alle Werte endlich, index > 0.
    Gibt (coefficients, root_index) zurück.
    """

    radicand = rational.comprehend(radicand)
    radicand = radicand.simplify()
    if isinstance(radicand, rational) and radicand.denominator == 1:
        radicand = radicand.numerator

    index = rational.comprehend(index)
    index = index.simplify()

    if isinstance(index, int):
        e = index
        coeffs = [-radicand] + [0]*(e-1) + [1]
        root_index = 0
        return coeffs, root_index

    p, q = index.numerator, index.denominator
    coeffs = [-radicand] + [0]*(p*q - 1) + [1]
    root_index = 0
    return coeffs, root_index


from typing import List, Union

def rational_root_candidates(coeffs: PolynomialCoefficients) -> List['rational']:
    """
    Liefert alle rationalen Kandidaten p/q für p|a0, q|an.
    coeffs: [a0, a1, ..., an] Koeffizienten des Polynoms
    """
    from math import gcd

    a0 = coeffs[0]
    an = coeffs[-1]

    def divisors(n):
        n = abs(n)
        return [i for i in range(1, n+1) if n % i == 0]

    ps = divisors(a0)
    qs = divisors(an)

    candidates = []
    for p in ps:
        for q in qs:
            candidates.append(rational(p, q))
            candidates.append(rational(-p, q))
    # Eindeutige Kandidaten
    seen = set()
    unique_candidates = []
    for c in candidates:
        key = (c.numerator, c.denominator)
        if key not in seen:
            seen.add(key)
            unique_candidates.append(c)
    return unique_candidates


def find_real_algebraic_roots(coeffs: PolynomialCoefficients) -> List[Union['rational','algebraic']]:
    """
    Findet alle rationalen Lösungen eines Polynoms mit rationalen Koeffizienten.
    coeffs: [a0, a1, ..., an], a0*x^0 + ... + an*x^n = 0
    Gibt sortierte Liste zurück. Wenn keine rationale Lösung existiert, 
    kann eine symbolische Algebraic-Repräsentation zurückgegeben werden.
    """
    # Kandidaten prüfen
    candidates = rational_root_candidates(coeffs)
    solutions: list[int | rational] = []

    for r in candidates:
        val = sum(c * (r ** i) for i, c in enumerate(coeffs))
        if val == 0:
            solutions.append(r.simplify())

    # Sortieren nach Wert
    solutions.sort(key=lambda x: x)
    
    if solutions:
        return solutions
    else:
        # Keine rationale Lösung gefunden, Minimalpolynom symbolisch zurückgeben
        # z.B. als Algebraic-Objekt mit root_index 0
        return [algebraic(coefficients=coeffs, root_number=0)]
