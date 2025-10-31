from typing import TypeVar, Callable, Any

from ametrine.library.numeric import Numeric

sourceType = TypeVar("sourceType")
convertedType = TypeVar("convertedType")

simplifyer: dict[sourceType, tuple[Callable[[sourceType], bool], Callable[[sourceType], convertedType]]] = {
    float: (
        lambda x: isinstance(x, float) and x.is_integer(),
        lambda x: int(x)
    ),
    int: (
        lambda x: True,
        lambda x: x
    )
}

def simplify(obj: Numeric | float | int | Any) -> Numeric | int | Any:
    """Vereinfacht ein Objekt so weit wie möglich."""
    input = obj

    current = obj
    last = None
    while type(current) != type(last):
        last = current

        if isinstance(current, Numeric):
            if current.reduce() is not None:
                current = current.reduce()

        elif type(current) in simplifyer:
            if simplifyer[type(current)][0](current):
                current = simplifyer[type(current)][1](current)

        else:
            current = current



    return current