from functools import wraps
from typing import Callable
from inspect import signature, isclass, isfunction


__all__ = ['check_func_args', 'check_class_args', 'get_callable_type']


def check_func_args(func):
    """
    @brief: 检查func的参数是否合法

    @param func: 函数

    @example:
    >>> @check_func_args
    >>> def my_func(a: int, b: str):
    >>>     pass
    >>>
    >>> my_func(1, '2')
    >>> my_func(1, 2)
    TypeError: Argument b must be str, not int
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)
        bound_args = sig.bind(*args, **kwargs)
        for name, value in bound_args.arguments.items():
            param = sig.parameters[name]
            if param.annotation != param.empty and not isinstance(value, param.annotation) and value != param.default:
                raise TypeError(f"Argument {name} must be {param.annotation.__name__}, not {type(value).__name__}")
        return func(*args, **kwargs)

    return wrapper


def check_class_args(cls):
    """
    @brief: 检查class的参数是否合法

    @param cls: 需要检查参数的类

    @example:
    >>> @check_class_args
    >>> class MyClass:
    >>>     def __init__(self, a: int, b: str):
    >>>         pass
    >>>     def my_method(self, c: int, d: str):
    >>>         pass
    >>>
    >>> my_class = MyClass(1, '2')
    >>> my_class = MyClass(1, 2)
    TypeError: Argument b must be str, not int
    >>> my_class.my_method(1, '2')
    >>> my_class.my_method(1, 2)
    TypeError: Argument d must be str, not int
    """
    for name, value in cls.__dict__.items():
        if isinstance(value, Callable):
            setattr(cls, name, check_func_args(value))
    return cls


def get_callable_type(func_or_class):
    if isfunction(func_or_class):
        return 'function'
    elif isclass(func_or_class):
        return 'class'
    else:
        raise TypeError(f"Expected a function or class, got {type(func_or_class).__name__}")
