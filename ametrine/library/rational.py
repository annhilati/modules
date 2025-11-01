from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias

from math import gcd, frexp

from ametrine.library.numeric import ExactNumber
from ametrine.ausgelagert import simplify
from ametrine.typing import Digit


@dataclass
class rational(ExactNumber):
    """Type, storing a rational number, meaning that it is arithmetically displayable by an division of two integers.
    
    Supported Magic
    --------
    - `+`, `-`, `*`, `/` for all `rational` and `rationalComprehendable` numbers
    - `**` as long as the exponent is an integer
    - `==`, `<`, `>`, `<=`, `>=`, 
    """
    numerator:      int
    denominator:    int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.numerator, int) or not isinstance(self.denominator, int):
            raise TypeError("Please ensure to instantiate `raional` type only with integers")

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

        Supported Types
        ---------
            **int** : No restrictions<br>
            **float** : Floats can loose accuracy after only a few decimals, thus they will be rounded to 15 decimals places<br>
            **str** : Has to be in the format `f"{whole}.{fraction}"`, whereby `whole` and `fraction` are consecutive digits

        Raises
        ---------
        TypeError : If it is not known how to express the given object as a rational 
        """
        if isinstance(obj, int):
            return cls(obj, 1)
        elif isinstance(obj, float):
            n, d = rational_parts_from_float(obj)
            return cls(n, d).round(15)
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
            raise TypeError(f"Cannot convert type to 'rational': '{type(obj).__name__}'")

    def __repr__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"
    
    def reduce(self) -> int | None:
        "Returns the rational as an `int` if it is whole, else `None`."
        if self.denominator == 1:
            return self.numerator
        return None
    
    def reciproke(self) -> rational:
        "Returns a new instance of the rational, whereby its numerator and denominator are swapped."
        return rational(
            numerator=self.denominator,
            denominator=self.numerator
        )

    def round(self, precision: int) -> rational:
        "Returns a new instance of the rational, rounded to `precision` decimals."
        whole, non_repeating, repeating = self.to_decimal_parts()
        decimals = "".join([str(d) for d in non_repeating]) + "".join([str(d) for d in repeating]) * (precision + 1)
        if precision >= len(decimals):
            return rational(self.numerator, self.denominator)

        nDecimals = decimals[:precision]

        if int(decimals[precision]) >= 5:

            nDecimals_list = list(nDecimals)
            nDecimals_list[-1] = str(int(nDecimals_list[-1]) + 1)
            nDecimals = "".join(nDecimals_list)

        return rational.comprehend(str(whole) + "." + nDecimals)
    
    def __add__(self, other):
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            return rational(numerator=self.numerator * other.denominator + other.numerator * self.denominator, denominator=self.denominator * other.denominator)
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
            other = rational.comprehend(other)
            if other.reduce() is not None:
                r = rational(
                    numerator=self.numerator ** abs(other.reduce()),
                    denominator=self.denominator ** abs(other.reduce())
                )
                return r if not other.is_negative else r.reciproke()
            else:
                raise NotImplementedError
        else:
            raise TypeError(f"unsupported operand type(s) for **: {type(self).__name__} and {type(other).__name__}")
        
    def __rpow__(self, other):
        other = simplify(other)
        if isinstance(other, rationalComprehendable):
            other = rational.comprehend(other)
            if other.reduce() is not None:
                r = rational(
                    numerator=self.numerator ** abs(other.reduce()),
                    denominator=self.denominator ** abs(other.reduce())
                )
                return r if not other.is_negative else r.reciproke()
            else:
                raise NotImplementedError
        else:
            raise TypeError(f"unsupported operand type(s) for **: {type(self).__name__} and {type(other).__name__}")

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
        "Expresses the rational as a tuple of the whole part, the non-repeating decimals as a list and the repeating decimals as a list."
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

        return (integer_part, non_repeating, repeating)
    
def rational_parts_from_float(f: float) -> tuple[int, int]:
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

rationalComprehendable: TypeAlias = int | float | str | rational