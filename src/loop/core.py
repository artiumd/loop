from typing import Iterable, Iterator, TypeVar, Generic


T = TypeVar('T')


class Loop(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable

    def __iter__(self) -> Iterator[T]:
        for inp in self._iterable:
            yield inp


def loop_over(iterable: Iterable[T]) -> Loop[T]:
    """Construct a new `Loop`.

    Customize the looping behaviour by chaining different `Loop` methods and finally use a `for` statement like you normally would.
    """
    return Loop(iterable)
