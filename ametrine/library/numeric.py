class Numeric:

    def reduce(self):
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
    