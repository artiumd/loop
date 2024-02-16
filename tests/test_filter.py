from src.loop import loop_over

from .utilities import assert_loop_raises, assert_loops_as_expected


def test_non_callable():
    loop = loop_over(range(10)).filter('no callable')
    assert_loop_raises(loop, TypeError)


def test_wrong_signature():
    def kwargs_only(**kwargs):
        pass

    loop = loop_over(range(10)).filter(kwargs_only)
    assert_loop_raises(loop, TypeError)


def test_empty():
    for _ in loop_over(range(10)).filter(lambda x: False):
        assert False


def test_all_true():
    inp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    loop = loop_over(inp).filter(lambda x: True)
    assert_loops_as_expected(loop, inp)


def test_even():
    out = [0,2,4,6,8]
    loop = loop_over(range(10)).filter(lambda x: x%2==0)
    assert_loops_as_expected(loop, out)
    

def test_greater_than_five():
    inp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    out = [x for x in inp if x > 5]
    loop = loop_over(inp).filter(lambda x: x > 5)
    assert_loops_as_expected(loop, out)


def test_isinstance_string():
    inp = [1, None, 'string', str, 1.1, 'str', []]
    out = ['string', 'str']
    loop = loop_over(inp).filter(isinstance, str)
    assert_loops_as_expected(loop, out)


def test_start_unpack():
    inp = [[1,3], [2,2], [6.0,6], [5,4]]
    out = [2,6]
    loop = loop_over(inp).next_call_with(unpacking='*').filter(lambda a,b: a==b).map(lambda x: x[0])
    assert_loops_as_expected(loop, out)


def test_dict_unpack():
    inp = [{'a': 1, 'b': 2}, {'c': 2, 'd': 5}, {'a': 3, 'e': 6},  {'f': 7}]
    out = [x for x in inp if 'a' in x]
    loop = loop_over(inp).next_call_with(unpacking='**').filter(lambda **kwargs: 'a' in kwargs)
    assert_loops_as_expected(loop, out)
