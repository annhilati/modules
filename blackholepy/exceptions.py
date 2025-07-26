class BlackHolePyError(Exception):
    ...

class DimensionError(BlackHolePyError):
    pass

class UnsupportedTerm(BlackHolePyError):
    pass