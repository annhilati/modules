from decimal import Decimal, getcontext
from ametrine.typing import PolynomialCoefficients
import cmath

def polynomial_roots(coeffs: PolynomialCoefficients, precision: int = 30):
    """
    Berechnet alle (komplexen) Wurzeln eines Polynoms
    a_0 + a_1*x + ... + a_n*x^n = 0
    mit Durand-Kerner-Verfahren auf n Nachkommastellen genau.
    """
    getcontext().prec = precision + 5  # etwas Sicherheitsreserve

    n = len(coeffs) - 1
    if n < 1:
        raise ValueError("Mindestens ein Koeffizient ungleich Null nötig")

    # in komplexe Koeffizienten umwandeln
    coeffs = [complex(Decimal(c)) for c in coeffs]

    def P(x):
        """Polynomwert P(x)"""
        s = complex(0)
        for i, a in enumerate(coeffs):
            s += a * (x ** i)
        return s

    # Startwerte gleichmäßig auf dem Einheitskreis
    roots = [complex(cmath.exp(2j * cmath.pi * k / n)) for k in range(n)]

    # Iteration
    for _ in range(precision * 5):  # max. Iterationen
        new_roots = []
        for i, x in enumerate(roots):
            denom = 1
            for j, y in enumerate(roots):
                if i != j:
                    denom *= (x - y)
            new_x = x - P(x) / denom
            new_roots.append(new_x)
        if max(abs(new_roots[i] - roots[i]) for i in range(n)) < Decimal(10) ** (-precision):
            break
        roots = new_roots

    # gerundete Ausgabe
    rounded = [
        complex(round(r.real, precision), round(r.imag, precision))
        for r in roots
    ]
    return rounded