from typing import TypeVar, Iterable, Type

import pytest

from src.loop import Loop


T = TypeVar('T')


def assert_loops_as_expected(loop: Loop[T], expected: Iterable[T]) -> None:
    actual = list(loop)
    expected = list(expected)
    assert actual == expected


def assert_loop_raises(loop: Loop[T], exception: Type[BaseException]) -> None:
    with pytest.raises(exception):
        for _ in loop:
            pass
