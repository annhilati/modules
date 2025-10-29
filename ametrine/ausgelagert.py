from typing import TypeVar, Callable, Any

sourceType = TypeVar("sourceType")
convertedType = TypeVar("convertedType")
T = TypeVar("T")

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

def simplify(obj: T) -> T | Any:
    """Vereinfacht ein Objekt so weit wie möglich."""
    while True:
        t = type(obj)

        if t in simplifyer:
            check, convert = simplifyer[t]
            if check(obj):
                new_obj = convert(obj)
                if type(new_obj) is t and new_obj == obj:
                    break
                obj = new_obj
                continue  # nochmal prüfen
            else:
                break

        elif hasattr(obj, "simplify"):
            new_obj = obj.simplify()
            if new_obj == obj:
                break
            obj = new_obj
            continue

        else:
            raise TypeError(
                f"Unknown numeric type: '{type(obj).__name__}'"
            )

    return obj
