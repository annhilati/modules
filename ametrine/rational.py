from __future__ import annotations
from dataclasses import dataclass

from math import gcd, frexp

from ametrine.ausgelagert import simplify


@dataclass
class rational:
    numerator:      int
    denominator:    int = 1

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
    def comprehend(cls, obj: rationalComprehendable) -> rational:
        "Don't use floats that are meant to be periodically"
        if isinstance(obj, int):
            return cls(obj, 1)
        elif isinstance(obj, float):
            n, d = float_to_rational(obj)
            return cls(n, d)
        elif isinstance(obj, rational):
            return cls(obj.numerator, obj.denominator)

    def __repr__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
    
    def __add__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=self.numerator * other.denominator + other.numerator * self.denominator,
                denominator=self.denominator * other.denominator
            )
        else:
            raise NotImplementedError
                
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=self.numerator * other.denominator - other.numerator * self.denominator,
                denominator=self.denominator * other.denominator
            )
        else:
            raise NotImplementedError
        
    def __rsub__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=other.numerator * self.denominator - self.numerator * other.denominator,
                denominator=self.denominator * other.denominator
            )
        else:
            raise NotImplementedError
        
    def __mul__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=self.numerator * other.numerator,
                denominator=self.denominator * other.denominator
            )
        else:
            raise NotImplementedError
        
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __truediv__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=self.numerator * other.denominator,
                denominator=self.denominator * other.numerator
            )
        else:
            raise NotImplementedError
        
    def __rtruediv__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=other.numerator * self.denominator,
                denominator=other.denominator * self.numerator
            )
        else:
            raise NotImplementedError
        
    def __pow__(self, exponent):
        exponent = simplify(exponent)
        # if isinstance(exponent, float):
        #     exponent = rational.comprehend(exponent)
        if isinstance(exponent, int):
            return rational(
                numerator=self.numerator ** exponent,
                denominator=self.denominator ** exponent
            )
        elif isinstance(exponent, rational):
            from ametrine.algebraic import root
            return simplify(root(
                radicand=self ** exponent.numerator,
                exponent=exponent.denominator
            ))
        else:
            raise NotImplementedError
        
    def __rpow__(self, base):
        base = simplify(base)
        # if isinstance(exponent, float):
        #     exponent = rational.comprehend(exponent)
        if isinstance(base, int) or isinstance(base, rational):
            from ametrine.algebraic import root
            return root(
                radicand=base ** self.numerator,
                exponent=self.denominator
            )
        else:
            raise NotImplementedError

    def __neg__(self):
        return rational(
            numerator=-self.numerator,
            denominator=self.denominator
        )
        
    def __eq__(self, value):
        value = simplify(value)
        if isinstance(value, rational):
            return self.numerator == value.numerator and self.denominator == value.denominator
        elif isinstance(value, rationalComprehendable):
            value = rational.comprehend(value)
            return self.numerator == value.numerator and self.denominator == value.denominator
        else:
            raise NotImplementedError(type(value))
        
    def __lt__(self, other):
        other = rational.comprehend(other)
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):
        other = rational.comprehend(other)
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):
        other = rational.comprehend(other)
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other):
        other = rational.comprehend(other)
        return self.numerator * other.denominator >= other.numerator * self.denominator
        
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
    
    def simplify(self) -> rational | int:
        if self.denominator == 1:
            return self.numerator
        return self
    
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
    m, e = frexp(f)

    numerator = int(m * 2**53)
    denominator = 2**53
    if e > 0:
        numerator <<= e
    else:
        denominator <<= -e

    g = gcd(numerator, denominator)
    return (numerator // g, denominator // g)

rationalComprehendable = int | float | rational