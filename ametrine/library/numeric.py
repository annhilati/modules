from __future__ import annotations
from typing import Self, Any

class ExactNumber:

    _immutable = False
    def __setattr__(self, name, value):
        if name in ["denominator", "numerator", "root_number", "coefficients", "radicand", "index"] and self._immutable:
            raise Exception(f"{type(self).__name__} is immutable")
        super().__setattr__(name, value)

    def __repr__(self):
        if type(self.eval()) == type(self):
            return self._repr()
        return str(self.eval()) 
        
    def eval(self):
        "Returns the most domain reduced repräsentation of this number"
        if (reduced := self.reduce()) is not None:
            if type(reduced) is ExactNumber:
                return reduced.eval()
            return reduced
        return self

    def reduce(self):
        raise NotImplementedError
        
    def _repr(self) -> str:
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

    def abs(self):
        raise NotImplementedError
    def negate(self):
        raise NotImplementedError
    
    @property
    def is_negative(self) -> bool:
        raise NotImplementedError
    