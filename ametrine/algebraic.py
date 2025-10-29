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
        if self.degree == 1:
            a0, a1 = self.coefficients
            if a1 != 0:
                return str(rational(-a0, a1))
        elif self.degree == 2:
            a, b, c = self.coefficients[2], self.coefficients[1], self.coefficients[0]
            disc = b**2 - 4*a*c
            sign = 1 if self.root_index == 0 else -1

            # Bruch + Wurzel vereinfachen
            k, r, denom = self.simplify_sqrt_div(disc, 2*a)
            if sign < 0:
                k = -k

            # if r == 1: # Bitte noch implementieren
            #     return f"{str(k) + "*" if k != 1 else ""}{"sqrt(" + str(r) + ")" if r != 1 else "1"}{"/" + str(denom) if denom != 1 else ""}"
            return f"{str(k) + "*" if k != 1 else ""}{"sqrt(" + str(r) + ")" if r != 1 else "1"}{"/" + str(denom) if denom != 1 else ""}"
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
    
    def simplify(self):
        """Gibt eine rationale Darstellung zurück, falls das Algebraic rational ist.
        Andernfalls wird self zurückgegeben.
        # TODO: Gibt teilweise negative Werte zurück, ergibt garkeinen Sinn. Teste: print(rational(5) ** rational(1, 2))
        """
        coeffs = self.coefficients
        root_index = self.root_index

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
                print(r)
                val = sum(c * (r ** i) for i, c in enumerate(coeffs))
                print(val)
                if val == 0:
                    # passende rationale Wurzel gefunden
                    # root_index wählt die Lösung (0 = erste, 1 = zweite, ...)
                    if root_index == 0:
                        return rational(r.numerator, r.denominator)

        return self  # keine rationale Lösung gefunden

    
    @property
    def rational(self) -> bool:
        coeffs = self.coefficients
        a_n = coeffs[-1]
        a_0 = coeffs[0]

        # mögliche p/q-Kandidaten
        ps = [i for i in range(-abs(a_0), abs(a_0)+1) if i != 0 and a_0 % i == 0]
        qs = [i for i in range(1, abs(a_n)+1) if a_n % i == 0]

        for p in ps:
            for q in qs:
                r = rational(p, q)
                val = sum(c * (r**i) for i, c in enumerate(coeffs))
                if val == 0:
                    return True, r
        return False, None

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
        return super().__mul__()
        
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