from src.loop import loop_over

from .utilities import assert_loops_as_expected, assert_loop_raises


def test_empty():
    assert_loops_as_expected(loop_over([]), [])


def test_range():
    assert_loops_as_expected(loop_over(range(1, 100, 2)), range(1, 100, 2))


def test_type_error():
    assert_loop_raises(loop_over(10), TypeError)
