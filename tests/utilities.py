from typing import Iterable, Type

import pytest

from src.loop import Loop


def assert_loops_as_expected(loop: Loop, expected: Iterable) -> None:
    actual = list(loop)
    expected = list(expected)
    assert actual == expected


def assert_loop_raises(loop: Loop, exception: Type[BaseException]) -> None:
    with pytest.raises(exception):
        for _ in loop:
            pass
