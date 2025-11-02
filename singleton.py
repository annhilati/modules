def singleton(instance_name: str = ..., /, *, immutable: bool = False):
    def decorator(cls):

        def __new__(cls):
            if cls._instance is None:
                cls._instance = object.__new__(cls)
            return cls._instance
        
        def __str__(self) -> str:
            return instance_name if instance_name is not ... else type(self).__name__
        
        def __setattr__(self, name, value) -> None:
            if immutable:
                raise AttributeError("Singleton is immutable")
            object.__setattr__(self, name, value)
        
        __new__.__doc__ = cls.__doc__

        setattr(cls, "_instance", None)
        setattr(cls, "__new__", __new__)
        setattr(cls, "__str__", __str__)
        setattr(cls, "__setattr__", __setattr__)

        return cls
    return decorator