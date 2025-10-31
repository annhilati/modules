from __future__ import annotations
from dataclasses import dataclass

from math import gcd, frexp

from ametrine.library.numeric import Numeric
from ametrine.ausgelagert import simplify
from ametrine.typing import Digit


@dataclass
class rational(Numeric):
    numerator:      int
    denominator:    int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.numerator, int) or not isinstance(self.denominator, int):
            raise TypeError

        if self.denominator == 0:
            raise ValueError("Denominator can't be zero")
        elif self.denominator < 0:
            self.numerator = - self.numerator
            self.denominator = - self.denominator
        
        g = gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // g
        self.denominator = self.denominator // g

    @classmethod
    def comprehend(cls, obj: rationalComprehendable) -> rational:
        """
        Don't use floats that are meant to be periodically or are longer than 16 decimals
        <br>floats lose accuracy after 16 decimals
        """
        if isinstance(obj, int):
            return cls(obj, 1)
        elif isinstance(obj, float):
            n, d = float_to_rational(obj)
            return cls(n, d)
        elif isinstance(obj, rational):
            return cls(obj.numerator, obj.denominator)
        elif isinstance(obj, str):
            if "." in obj:
                objWhole, objFrac = obj.split(".", 1)
                frac = rational(int(objFrac), 10 ** len(objFrac))
                whole = rational(int(objWhole))
                return frac + whole
            return rational(int(obj))
        else:
            raise TypeError(obj)
            raise TypeError(f"Cannot convert type to 'rational': '{type(obj).__name__}'")

    def __repr__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
    
    def reduce(self) -> int | None:
        if self.denominator == 1:
            return self.numerator
        return None

    def round(self, to_decimals: int) -> rational:
        whole, non_repeating, repeating = self.to_decimal_parts()
        decimals = "".join([str(d) for d in non_repeating]) + "".join([str(d) for d in repeating]) * (to_decimals + 1)
        if to_decimals >= len(decimals):
            return rational(self.numerator, self.denominator)

        nDecimals = decimals[:to_decimals]  # die ersten to_decimals Zeichen
        # Prüfen, ob gerundet werden muss
        if int(decimals[to_decimals]) >= 5:
            # Umwandeln in Liste, letzte Stelle erhöhen
            nDecimals_list = list(nDecimals)
            nDecimals_list[-1] = str(int(nDecimals_list[-1]) + 1)
            nDecimals = "".join(nDecimals_list)

        return rational.comprehend(str(whole) + "." + nDecimals)
    
    def __add__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=self.numerator * other.denominator + other.numerator * self.denominator,
                denominator=self.denominator * other.denominator
            )
        else:
            raise NotImplementedError(f"unsupported operand type(s) for +: {type(self).__name__} and {type(other).__name__}")
                
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
            raise TypeError(f"unsupported operand type(s) for -: {type(self).__name__} and {type(other).__name__}")
        
    def __rsub__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=other.numerator * self.denominator - self.numerator * other.denominator,
                denominator=self.denominator * other.denominator
            )
        else:
            raise TypeError(f"unsupported operand type(s) for -: {type(other).__name__} and {type(self).__name__}")
        
    def __mul__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=self.numerator * other.numerator,
                denominator=self.denominator * other.denominator
            )
        else:
            raise TypeError(f"unsupported operand type(s) for *: {type(self).__name__} and {type(other).__name__}")
        
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
            raise TypeError(f"unsupported operand type(s) for /: {type(self).__name__} and {type(other).__name__}")
        
    def __rtruediv__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(
                numerator=other.numerator * self.denominator,
                denominator=other.denominator * self.numerator
            )
        else:
            raise TypeError(f"unsupported operand type(s) for /: {type(other).__name__} and {type(self).__name__}")
        
    def __pow__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(rational)
            from ametrine.library.algebraic import root
            return simplify(root(
                radicand=rational(
                    numerator=self.numerator ** other.numerator,
                    denominator=self.denominator ** other.denominator
                ),
                index=other.denominator
            ))
        else:
            raise TypeError(f"unsupported operand type(s) for **: {type(self).__name__} and {type(other).__name__}")
        
    def __rpow__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(rational)
            from ametrine.library.algebraic import root
            return simplify(root(
                radicand=rational(
                    numerator=other.numerator ** self.numerator,
                    denominator=other.denominator ** self.denominator
                ),
                index=self.denominator
            ))
        else:
            raise TypeError(f"unsupported operand type(s) for /: {type(other).__name__} and {type(self).__name__}")

    def __neg__(self):
        return rational(
            numerator=-self.numerator,
            denominator=self.denominator
        )
        
    def __eq__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return self.numerator == other.numerator and self.denominator == other.denominator
        
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
    def is_negative(self) -> bool:
        return self.numerator < 0
    
    @property
    def is_periodic(self) -> bool:
        return len(self.to_decimal_parts()[-1]) != 0
    
    def to_decimal_parts(self) -> tuple[int, list[Digit], list[Digit]]:
        "Can have leading zeros!"
        integer_part = self.numerator // self.denominator
        remainder = abs(self.numerator % self.denominator)

        if remainder == 0:
            return integer_part, [], []

        seen = {}
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

rationalComprehendable = int | float | rational | str