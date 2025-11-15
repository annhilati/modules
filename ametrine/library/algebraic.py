from __future__ import annotations

from dataclasses import dataclass, field
from ametrine.library.rational import rational, rationalComprehendable
from ametrine.library.numeric import ExactNumber
from ametrine.typing import PolynomialCoefficients

@dataclass
class algebraic(ExactNumber):
    """Type, storing an algebraic number, meaning that it is algebraically representable by a polynomials coefficients and the number of the corresponding solution of this polynomial.
    
    Supported Magic
    --------
    - ...
    """
    coefficients:   PolynomialCoefficients
    root_number:    int         = 0

    def __post_init__(self):
        if any([not isinstance(coefficient, int) for coefficient in self.coefficients]):
            raise TypeError
        
        if len(self.coefficients) < 2:
            raise ValueError

    def __repr__(self) -> str:
        return f"<{self.root_number + 1}. solution of the polynomial '0 = {' + '.join(f'{c}x^{i}' for i, c in enumerate(self.coefficients))}'>"
    
    def __add__(self, oher):
        ...
    
    @property
    def polynomial_degree(self) -> int:
        return len(self.coefficients) - 1

    @property
    def is_rational(self) -> bool:
        ...

    @property
    def determinant(self) -> rational:
        ...

@dataclass
class radical(ExactNumber):
    """Type, storing an radical number, meaning that it is algebraically displayable as a radical expression.
    
    Supported Magic
    --------
    - ...
    """
    radicand:       rational
    index:          rational

    def __post_init__(self):
        index = self.index
        self.index = index.numerator
        self.radicand = self.radicand ** index.denominator

    def __repr__(self) -> str:
        return f"<{self.index}. root of {self.radicand}>"
    
    def as_algebraic(self) -> algebraic:
        ...

rootComprehendable = rationalComprehendable
        
def algebraic_from_root(radicand: rationalComprehendable, index: rationalComprehendable):
    """
    Bestimmt das Minimalpolynom und den Lösungsindex einer algebraischen Zahl x = radicand^(1/index).
    Annahme: kein Fehlerfall, alle Werte endlich, index > 0.
    Gibt (coefficients, root_index) zurück.
    """

    radicand = rational.comprehend(radicand)
    radicand = radicand.eval()
    if isinstance(radicand, rational) and radicand.denominator == 1:
        radicand = radicand.numerator

    index = rational.comprehend(index)
    index = index.eval()

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
