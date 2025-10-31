# Beispiel: funktioniert mit fractions.Fraction. 
# Ersetze rat_factory durch deinen Rational-Konstruktor:
from ametrine.library.rational import rational

# Binary splitting für Terms (-1)^k / ((2k+1)*m^(2k+1))
def bs_arctan_range(m, a, b):
    # gibt (P, Q) als Python ints zurück, die Summe = P/Q
    if b - a == 1:
        sign = -1 if (a % 2) else 1
        exp = 2*a + 1
        P = sign
        Q = (2*a + 1) * pow(m, exp)
        return P, Q
    mid = (a + b) // 2
    P1, Q1 = bs_arctan_range(m, a, mid)
    P2, Q2 = bs_arctan_range(m, mid, b)
    # (P1/Q1) + (P2/Q2) = (P1*Q2 + P2*Q1) / (Q1*Q2)
    P = P1 * Q2 + P2 * Q1
    Q = Q1 * Q2
    return P, Q

def arctan_rational(m, terms):
    # berechnet arctan(1/m) als rat(P, Q)
    P, Q = bs_arctan_range(m, 0, terms)
    return rational(P, Q)

import math
def terms_needed_for_m(m, n_digits):
    # grobe Abschätzung: nächster Term < 10^{-n_digits-1}
    # Term_k ≈ 1/((2k+1)*m^{2k+1}) <= 10^{-(n_digits+1)}
    # Löse grob nach k per log. Wir iterieren bis Bedingung erfüllt.
    target = 10 ** (-(n_digits + 1))
    k = 0
    while True:
        bound = 1.0 / ((2*k+1) * (m ** (2*k+1)))
        if bound < target:
            return k + 1  # Anzahl Terme = k+1
        k += 1

def compute_pi(n_digits):
    # n_digits: Anzahl gewünschter Dezimalstellen
    # rat_factory(num, den=1) -> dein Rational
    # liefert rationale Approximation von pi, korrekt auf n_digits
    # Machin: pi = 4*(4*arctan(1/5) - arctan(1/239))
    m1, m2 = 5, 239
    t1 = terms_needed_for_m(m1, n_digits)
    t2 = terms_needed_for_m(m2, n_digits)
    A1 = arctan_rational(m1, t1)   # arctan(1/5)
    A2 = arctan_rational(m2, t2)   # arctan(1/239)
    # pi = 4 * (4*A1 - A2)
    four = rational(4)
    pi_rat = four * ( four * A1 - A2 )
    return pi_rat