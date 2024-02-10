import pytest

from src.loop import loop_over


def test_non_callable():
    with pytest.raises(TypeError):
        loop_over(range(10)).reduce('non callable')


def test_callable_one_arg():
    with pytest.raises(TypeError):
        loop_over(range(10)).reduce(lambda x: x)


def test_callable_two_arg_with_error():
    with pytest.raises(TypeError):
        loop_over(['hello', 'world']).reduce(lambda a,b: a @ b)


def test_single_item():
    def raise_error():
        raise TypeError

    result = loop_over([5]).reduce(raise_error)
    assert result == 5


def test_no_items_with_initializer():
    def raise_error():
        raise TypeError

    initializer = object()
    result = loop_over([]).reduce(raise_error, initializer)
    assert result is initializer


def test_no_items_not_initializer():
    with pytest.raises(TypeError):
        loop_over([]).reduce(lambda x, y: x+y)


def test_min_no_initializer():
    result = loop_over(range(10)).reduce(min)
    assert result == 0


def test_min_with_initializer():
    result = loop_over(range(10)).reduce(min, -1)
    assert result == -1


def test_sum():
    expected = sum(range(10))
    result = loop_over(range(10)).reduce(lambda x,y: x+y)
    assert expected == result
