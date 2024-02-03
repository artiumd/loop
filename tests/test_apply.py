from src.loop import loop_over

from .utilities import assert_loop_raises, assert_loops_as_expected


def test_apply_empty():
    assert_loops_as_expected(loop_over([]).apply(lambda x: None), [])


def test_apply_plus_one():
    assert_loops_as_expected(loop_over(range(1, 100, 2)).apply(lambda x: x + 1), range(2, 101, 2))


def test_apply_plus_one_then_plus_one():
    assert_loops_as_expected(loop_over(range(1, 100, 2)).apply(lambda x: x + 1).apply(lambda x: x + 1), range(3, 102, 2))


def test_apply_assert_on_args_kwargs():
    args = (1, 'a', False)
    kwargs = {'a': [], 'b': {}, 'c': None}

    def function(x, *args_, **kwargs_):
        assert args_ == args
        assert kwargs_ == kwargs
        return x

    assert_loops_as_expected(loop_over(range(10)).apply(function, *args, **kwargs), range(10))


def test_apply_type_error():
    assert_loop_raises(loop_over(range(10)).apply('not a function'), TypeError)


def test_apply_error_in_function():
    def raise_error(x):
        raise RuntimeError

    assert_loop_raises(loop_over(range(10)).apply(raise_error), RuntimeError)


def test_apply_wrong_signature():
    def takes_two(one, two):
        return one

    assert_loop_raises(loop_over(range(10)).apply(takes_two), TypeError)


def test_unpack_apply():
    assert_loops_as_expected(loop_over([[1,2], [4,7], [9,15], [6,6]]).unpack_apply(lambda x, y: x + y), [3,11,24,12])