from typing import Callable, TypeVar, Iterable


T = TypeVar('T')
R = TypeVar('R')


class DummyPool:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def imap(self, fn: Callable[[T], R], iterable: Iterable[T], chunksize=None) -> Iterable[R]:
        return map(fn, iterable)
