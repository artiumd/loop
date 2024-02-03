from src.loop import loop_over

from .utilities import assert_loop_raises, assert_loops_as_expected


def test_empty():
    def raise_error(x):
        raise RuntimeError

    for _  in loop_over([]).apply(raise_error):
        assert False


def test_plus_one():
    inp = [1, 2, 3, 4, 5, 6, 7, 8]
    out = [x + 1 for x in inp]
    assert_loops_as_expected(loop_over(inp).apply(lambda x: x + 1), out)


def test_times_two_plus_one():
    inp = [1, 2, 3, 4, 5, 6, 7, 8]
    out = [(2 * x) + 1 for x in inp]
    assert_loops_as_expected(loop_over(inp).apply(lambda x: 2*x).apply(lambda x: x + 1), out)


def test_plus_one_times_two():
    inp = [1, 2, 3, 4, 5, 6, 7, 8]
    out = [(x + 1) * 2 for x in inp]
    assert_loops_as_expected(loop_over(inp).apply(lambda x: x + 1).apply(lambda x: 2*x), out)


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