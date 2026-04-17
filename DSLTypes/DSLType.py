"""
DSL types are a special kind of typing types that come with tooling for automatic parsing of arguments in functions.

Essentially, they are like typing with Unions, but:
1. with the help of a decorator, functions where a DSLtype is used in a annotation, the argument value will be coherced in a way defined by the user
2. IDE will display only coherce types attributes

"""


from typing import Callable, Any, get_args, get_origin, get_type_hints, overload, Iterable, Union
import functools, inspect, types

class DSLMeta(type):

    @property
    def _dsl_result_type_(cls) -> type:
        return cls.__bases__[1]
    
    _allowed = {"__bases__", "_dsl_result_type_", "parse"}
    # Später so ersetzen, dass alles verboten ist, was in _dsl_result_type_ vorkommt, nicht aber in cls

    def __getattribute__(cls, name):
        if name not in DSLMeta._allowed:
            raise AttributeError(f"you mistakenly queried an attribute {name} of a DSLType that belongs to another specific type")
        return type.__getattribute__(cls, name)


class DSLType(metaclass=DSLMeta):
    """
    
    ## Usage
    ```
    class number(DSLType, float):
        @classmethod
        def parse(cls, v: int | float | str) -> float:
            return float(v)
    ```
    """
    
    @classmethod
    def parse[V, T](cls, v: V, **kwargs) -> T:
        raise NotImplementedError("parse method not implemented")
    
    def __new__(cls, *args, **kwargs):
        raise Exception("don't instanciate DSLType classes")
    
    #======// Definition Validation //===========================================================//
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        try:
            if type(cls._dsl_result_type_) is not type:
                raise
        except IndexError:
            raise TypeError("the second argument of the class definition must be a type")
        
        try:
            cls.parse(0)
        except NotImplementedError:
            raise TypeError("parse method must be implemented")
        except Exception:
            pass
    
    
# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                   Decorator                                   │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯
    
class DSLMethod:
    """Use this decorator on functions to automatically resolve arguments annotated by a `DSLType`. 
    
    **NOTE:** Add description on what happens when using multiple DSLTypes alternatively
    """
     
    @overload # Overload 1: Benutzung ohne Klammern -> @Decorator
    def __new__[**P, R](cls, func: Callable[P, R]) -> Callable[P, R]: ...
    @overload # Overload 2: Benutzung mit Klammern -> @Decorator(key=...)
    def __new__(cls, func: None = None, **kwargs: Any) -> "DSLMethod": ...

    def __new__(cls, func=None, **kwargs):
        if callable(func) and not kwargs:
            return cls._make_wrapper(func, {})
        return super().__new__(cls)

    def __init__(self, func=None, **kwargs):
        self.kwargs = kwargs

    def __call__[**P, R](self, func: Callable[P, R]) -> Callable[P, R]:
        # Benutzung mit Klammern: Die Instanz wird auf die Funktion aufgerufen
        return self._make_wrapper(func, self.kwargs)

    @staticmethod
    def _make_wrapper[**P, R](func: Callable[P, R], deco_kwargs: dict[str, Any]) -> Callable[P, R]:
        sig = inspect.signature(func)
        hints = get_type_hints(func)

        def parse_value(val: Any, hint: Any) -> Any:
            """Rekursive Logik zur Typ-Konvertierung basierend auf DSLType."""
            origin = get_origin(hint)
            args = get_args(hint)

            # 1. Handle Union Types (z.B. int | DSLType oder Union[int, str])
            if origin is Union or isinstance(hint, types.UnionType):
                for arg in args:
                    try:
                        # Wir versuchen den Wert gegen jeden Typ in der Union zu parsen
                        return parse_value(val, arg)
                    except (TypeError, ValueError):
                        continue
                return val # Falls nichts passt, Originalwert

            # 2. Handle DSLType Subklassen ◄── Das Herzstück
            if isinstance(hint, type) and issubclass(hint, DSLType):
                return hint.parse(val)

            # 3. Rekursive Container-Prüfung
            try:
                if origin is list and args:
                    return [parse_value(v, args[0]) for v in val]
                
                if origin is set and args:
                    return {parse_value(v, args[0]) for v in val}
                
                if origin is tuple and args:
                    # Variadische Tupel: tuple[T, ...]
                    if len(args) == 2 and args[1] is Ellipsis:
                        return tuple(parse_value(v, args[0]) for v in val)
                    # Fixe Tupel: tuple[T1, T2]
                    return tuple(parse_value(v, a) for v, a in zip(val, args))
                
                if origin is dict and args:
                    k_hint, v_hint = args
                    return {parse_value(k, k_hint): parse_value(v, v_hint) for k, v in val.items()}
            except (TypeError, Iterable): # Falls val nicht iterierbar ist, obwohl der Hint es sagt
                return val

            return val

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            # Iteriere über alle gebundenen Argumente und wende parse_value an
            for name, value in bound.arguments.items():
                if name in hints:
                    # Ersetze das Argument durch das geparste Ergebnis ➔
                    bound.arguments[name] = parse_value(value, hints[name])

            return func(*bound.args, **bound.kwargs)

        return wrapper