from typing import Iterable, Iterator, TypeVar

from typing_extensions import Protocol


T = TypeVar('T')
A = TypeVar('A')
K = TypeVar('K')
R = TypeVar('R')


class Function(Protocol):
    def __call__(self, *args: A, **kwargs: K) -> R:
        ...


class FunctionApplier:
    __slots__ = ('_args', '_kwargs', '_function')

    def __init__(self, function: Function, *args: A, **kwargs: K):
        self._args = args
        self._kwargs = kwargs
        self._function = function

    def __call__(self, inp: T) -> R:
        return self._function(inp, *self._args, **self._kwargs)


class UnpackerFunctionApplier(FunctionApplier):
    __slots__ = ()

    def __call__(self, inp: T) -> R:
        return self._function(*inp, *self._args, **self._kwargs)


class Loop:
    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable
        self._functions = []

    def apply(self, function: Function, *args: A, **kwargs: K) -> 'Loop':
        """
        Apply `function` to each `item` in `iterable` by calling `function(item, *args, **kwargs)`.

        `apply()` may be called multiple times, this will cause multiple functions to be applied (in the same order).

        !!! note

            This is not the same as applying `functools.partial(function, *args, **kwargs)` to `item` because it would translate to `function(*args, item, **kwargs)`.
        """
        self._functions.append(FunctionApplier(function, *args, **kwargs))
        return self

    def unpack_apply(self, function: Function, *args: A, **kwargs: K) -> 'Loop':
        """
        This is the same as `apply()` except that the `item` from `iterable` is star unpacked as it is passed to `function` i.e. `function(*item, *args, **kwargs)`.
        """
        self._functions.append(UnpackerFunctionApplier(function, *args, **kwargs))
        return self

    def __iter__(self) -> Iterator[R]:
        for inp in self._iterable:
            out = inp

            for function in self._functions:
                out = function(out)

            yield out


def loop_over(iterable: Iterable[T]) -> Loop:
    """Construct a new `Loop`.

    Customize the looping behaviour by chaining different `Loop` methods and finally use a `for` statement like you normally would.
    """
    return Loop(iterable)
