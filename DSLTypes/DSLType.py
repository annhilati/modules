from typing import Callable, Any, get_args, get_origin, get_type_hints, overload
import functools, inspect

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
    
class Decorator:
     
    @overload # Overload 1: Benutzung ohne Klammern -> @Decorator
    def __new__[**P, R](cls, func: Callable[P, R]) -> Callable[P, R]: ...
    @overload # Overload 2: Benutzung mit Klammern -> @Decorator(key=...)
    def __new__(cls, func: None = None, **kwargs: Any) -> "Decorator": ...

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
    def _make_wrapper[**P, R](func: Callable[P, R], deco_kwargs: dict[str]) -> Callable[P, R]:
        sig = inspect.signature(func)
        hints = get_type_hints(func)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, value in list(bound.arguments.items()):
                ann = hints.get(name)
                # DSLType ist hier als Platzhalter für deine Basisklasse gedacht
                if isinstance(ann, type) and issubclass(ann, DSLType):
                    bound.arguments[name] = ann.parse(value, **deco_kwargs)

            return func(*bound.args, **bound.kwargs)

        return wrapper