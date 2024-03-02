from typing import Type, Callable, Union, TypeVar
from functools import wraps


class skipped:
    pass


def args_last_adapter(adaptee, *args, **kwargs):
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(inp, *args, **kwargs)

    return adapted


def args_first_adapter(adaptee, *args, **kwargs):
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*args, inp, **kwargs)

    return adapted


def tuple_unpack_args_last_adapter(adaptee, *args, **kwargs):
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*inp, *args, **kwargs)

    return adapted


def tuple_unpack_args_first_adapter(adaptee, *args, **kwargs):
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*args, *inp, **kwargs)

    return adapted


def dict_unpack_adapter(adaptee, *args, **kwargs):
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*args, **inp, **kwargs)
    
    return adapted


T = TypeVar('T')


def filter_adapter(adaptee: Callable[[T], bool]) -> Callable[[T], Union[T, Type[skipped]]]:
    @wraps(adaptee)
    def adapted(inp):
        out = adaptee(inp)

        if out:
            return inp
        else:
            return skipped

    return adapted
