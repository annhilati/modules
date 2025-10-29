from __future__ import annotations
from dataclasses import dataclass

from math import gcd, frexp

@dataclass
class rational:
    numerator:      int
    denominator:    int

    def __post_init__(self) -> None:
        if not isinstance(self.numerator, int) or not isinstance(self.denominator, int):
            raise TypeError

        if self.denominator == 0:
            raise ValueError("Denominator can't be zero")
        elif self.denominator < 0:
            raise ValueError("Denominator can't be below zero")
        
        g = gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // g
        self.denominator = self.denominator // g

    @classmethod
    def comprehend(cls, v: float) -> rational:
        n, d = float_to_rational(v)
        return cls(n, d)

    def __repr__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
    
    def __add__(self, other):
        if isinstance(other, rational):
            return rational(
                numerator=self.numerator * other.denominator + other.numerator * self.denominator,
                denominator=self.denominator * other.denominator
            )
        elif isinstance(other, int):
            return rational(
                numerator=self.numerator + other * self.denominator,
                denominator=self.denominator
            )
        else:
            raise TypeError
        
    def __mul__(self, other):
        if isinstance(other, rational):
            return rational(
                numerator=self.numerator * other.numerator,
                denominator=self.denominator * other.denominator
            )
        elif isinstance(other, int):
            return rational(
                numerator=self.numerator * other,
                denominator=self.denominator
            )
        else:
            raise TypeError
        
    @property
    def negative(self) -> bool:
        return self.numerator < 0
    
    @property
    def periodic(self) -> bool:
        d = self.denominator // gcd(self.numerator, self.denominator)
        for p in (2, 5):
            while d % p == 0:
                d //= p
        return d != 1
    
    def to_decimal_parts(self) -> tuple[int, int, int]:
        "Can have leading zeros!"
        integer_part = self.numerator // self.denominator
        remainder = abs(self.numerator % self.denominator)

        if remainder == 0:
            return integer_part, None, None

        seen = {}  # remainder -> position
        digits = []
        repeating_start = None

        while remainder != 0:
            if remainder in seen:
                repeating_start = seen[remainder]
                break
            seen[remainder] = len(digits)
            remainder *= 10
            digit = remainder // self.denominator
            digits.append(digit)
            remainder %= self.denominator

        if repeating_start is None:
            # kein periodischer Teil
            non_repeating = digits
            repeating = []
        else:
            non_repeating = digits[:repeating_start]
            repeating = digits[repeating_start:]

        # abschließende Nullen entfernen (nur aus dem nichtperiodischen Teil)
        while non_repeating and non_repeating[-1] == 0 and not repeating:
            non_repeating.pop()

        return (
            integer_part,
            non_repeating,
            repeating
        )


def float_to_rational(f: float):
    if f == 0.0:
        return (0, 1)
    m, e = frexp(f)  # f = m * 2**e, m in [0.5, 1)
    # Bruch aus Mantisse und Exponent
    numerator = int(m * 2**53)
    denominator = 2**53
    if e > 0:
        numerator <<= e
    else:
        denominator <<= -e
    # Kürzen
    from math import gcd
    g = gcd(numerator, denominator)
    return (numerator // g, denominator // g)