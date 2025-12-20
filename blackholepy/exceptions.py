class BlackHolePyError(Exception):
    "Base class for all BlackHolePy exceptions."
    ...

class CosmicCensorshipHypothesis(BlackHolePyError):
    "Raised when certain parameters violate the cosmic censorship hypothesis."
    ...

class LawOfConservationOfEnergy(BlackHolePyError):
    "Raised when certain parameters violate the law of conservation of energy."
    ...

class FaultyImplementation(BlackHolePyError):
    ...