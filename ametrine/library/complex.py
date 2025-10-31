from dataclasses import dataclass

from ametrine.library.numeric import Numeric
from ametrine.library.algebraic import algebraic, root

@dataclass
class complex(Numeric):
    real:      algebraic
    imaginary: algebraic


