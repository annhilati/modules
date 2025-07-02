from sympy import Expr, Mul, Add, Pow
from sympy.physics.units import Dimension
from sympy.physics.units.quantities import Quantity


def dimensions(expr: Expr) -> Dimension | list[Dimension]:
    """
    Returns a list of the physical dimensions of a Expr object when multiplied
    """

    dimensions = []

    for factor in expr.as_ordered_factors():
        if isinstance(factor, Quantity):
            dimensions.append(factor.dimension)

        elif isinstance(factor, Pow):
            base, exp = factor.as_base_exp()
            if isinstance(base, Quantity):  # Basis ist eine Einheit
                dimensions.append(base.dimension ** exp)

        elif isinstance(factor, Mul):  # Rekursive Zerlegung für verschachtelte Multiplikation
            sub_dimensions = dimensions(factor)
            dimensions.extend(sub_dimensions)

        elif isinstance(factor, Add):
            raise ValueError("Can't use additions of dimensions properly")

    if len(dimensions) == 1: dimensions = dimensions[0]
    return dimensions