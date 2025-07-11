class BlackHolyPyError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg

class DimensionError(BlackHolyPyError):
    pass

class UnsupportedTerm(BlackHolyPyError):
    pass