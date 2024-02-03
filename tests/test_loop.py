from src.loop import loop_over

from .utilities import assert_loops_as_expected, assert_loop_raises


def test_empty():
    for _ in loop_over([]):
        assert False


def test_range():
    inp = range(1, 100, 2)
    out = range(1, 100, 2)
    loop = loop_over(inp)
    assert_loops_as_expected(loop, out)


def test_type_error():
    loop = loop_over(10)
    assert_loop_raises(loop, TypeError)


def test_exhaust():
    inp = list(range(10))
    out = []
    result = loop_over(inp).map(out.append).exhaust()
    assert result is None
    assert out == inp
