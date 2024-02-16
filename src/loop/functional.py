from typing import TypeVar, Protocol, Type, Callable, TypeVar, Union
from functools import wraps

T = TypeVar('T')
A = TypeVar('A')
K = TypeVar('K')
R = TypeVar('R')


class skipped:
    pass


class ArgArgsKwargsFunction(Protocol):
    def __call__(self, arg: T, *args: A, **kwargs: K) -> R:
        ...


class ArgsArgKwargsFunction(Protocol):
    def __call__(self, *args: A, arg: T, **kwargs: K) -> R:
        ...


class ArgsKwargsFunction(Protocol):
    def __call__(self, *args: A, **kwargs: K) -> R:
        ...


class ArgsKwargsFunction(Protocol):
    def __call__(self, *args: A, **kwargs: K) -> R:
        ...


class OneArgFunction(Protocol):
    def __call__(self, arg: T) -> R:
        ...


def args_last_adapter(adaptee: ArgArgsKwargsFunction, *args: A, **kwargs: K) -> OneArgFunction:
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(inp, *args, **kwargs)

    return adapted


def args_first_adapter(adaptee: ArgsArgKwargsFunction, *args: A, **kwargs: K) -> OneArgFunction:
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*args, inp, **kwargs)

    return adapted


def tuple_unpack_args_last_adapter(adaptee: ArgsKwargsFunction, *args: A, **kwargs: K) -> OneArgFunction:
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*inp, *args, **kwargs)

    return adapted


def tuple_unpack_args_first_adapter(adaptee: ArgsKwargsFunction, *args: A, **kwargs: K) -> OneArgFunction:
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*args, *inp, **kwargs)

    return adapted


def dict_unpack_adapter(adaptee: ArgsKwargsFunction, *args: A, **kwargs: K) -> OneArgFunction:
    @wraps(adaptee)
    def adapted(inp):
        return adaptee(*args, **inp, **kwargs)
    
    return adapted


T = TypeVar('T')
R = TypeVar('R')


def filter_adapter(adaptee: Callable[[T], R]) -> Callable[[T], Union[R, Type[skipped]]]:
    @wraps(adaptee)
    def adapted(inp):
        out = adaptee(inp)

        if out:
            return inp
        else:
            return skipped

    return adapted
