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
    loop = loop_over(inp).apply(lambda x: x + 1)
    assert_loops_as_expected(loop, out)


def test_times_two_plus_one():
    inp = [1, 2, 3, 4, 5, 6, 7, 8]
    out = [(2 * x) + 1 for x in inp]
    loop = loop_over(inp).apply(lambda x: 2*x).apply(lambda x: x + 1)
    assert_loops_as_expected(loop, out)


def test_plus_one_times_two():
    inp = [1, 2, 3, 4, 5, 6, 7, 8]
    out = [(x + 1) * 2 for x in inp]
    loop = loop_over(inp).apply(lambda x: x + 1).apply(lambda x: 2*x)
    assert_loops_as_expected(loop, out)


def test_apply_assert_on_args_kwargs():
    args = (1, 'a', False)
    kwargs = {'a': [], 'b': {}, 'c': None}

    def function(x, *args_, **kwargs_):
        assert args_ == args
        assert kwargs_ == kwargs
        return x

    inp = range(10)
    out = range(10)
    loop = loop_over(inp).apply(function, *args, **kwargs)
    assert_loops_as_expected(loop, out)


def test_apply_type_error():
    inp = range(10)
    loop = loop_over(inp).apply('not a function')
    assert_loop_raises(loop, TypeError)


def test_apply_error_in_function():
    def raise_error(x):
        raise RuntimeError

    inp = range(10)
    loop = loop_over(inp).apply(raise_error)
    assert_loop_raises(loop, RuntimeError)


def test_apply_wrong_signature():
    def takes_two(one, two):
        return one

    inp = range(10)
    loop = loop_over(inp).apply(takes_two)
    assert_loop_raises(loop, TypeError)


def test_unpack_apply():
    inp = [[1,2], [4,7], [9,15], [6,6]]
    out = [3,11,24,12]
    loop = loop_over(inp).unpack_apply(lambda x, y: x + y)
    assert_loops_as_expected(loop, out)


def test_side_effects():
    inp = range(10)
    out = []

    def append_to_out(x):
        out.append(x)

    for _ in loop_over(inp).apply(append_to_out):
        pass

    assert out == list(inp)
