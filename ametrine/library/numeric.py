from __future__ import annotations

class ExactNumber:

    _immutable = False
    def __setattr__(self, name, value):
        if name in ["denominator", "numerator", "root_number", "coefficients", "radicand", "index"] and self._immutable:
            raise Exception(f"{type(self).__name__} is immutable")
        super().__setattr__(name, value)

    def reduce(self) -> ExactNumber | int | None:
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError
    def __sub__(self, other):
        raise NotImplementedError
    def __mul__(self, other):
        raise NotImplementedError
    def __truediv__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError
    def __lt__(self, other):
        raise NotImplementedError
    def __gt__(self, other):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def abs(self):
        raise NotImplementedError
    def negate(self):
        raise NotImplementedError
    
    @property
    def is_negative(self) -> bool:
        raise NotImplementedError
    