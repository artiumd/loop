from typing import Iterable, Optional, TypeVar, Iterator
from itertools import islice


T = TypeVar('T')


def batched(iterable: Iterable[T], n: Optional[int] = None) -> Iterator[Iterable[T]]:
    if n is None:
        yield iterable
    else:
        # Copied from: https://docs.python.org/3/library/itertools.html#itertools.batched
        it = iter(iterable)
        empty = True

        while batch := tuple(islice(it, n)):
            empty = False
            yield batch

        if empty:
            yield ()
