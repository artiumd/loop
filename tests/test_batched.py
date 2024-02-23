from itertools import zip_longest

from src.loop import batched


def test_empty():
    _test_batched([], n=None, expected=[[]])
    _test_batched([], n=1, expected=[[]])
    _test_batched([], n=100, expected=[[]])


def test_none():
    _test_batched([1,2,3], n=None, expected=[[1,2,3]])


def test_one():
    for n in range(10):
        _test_batched(range(n), n=1, expected=[[i] for i in range(n)] if n else [[]])


def test_divisible():
    _test_batched(range(12), n=3, expected=[[0,1,2], [3,4,5], [6,7,8], [9,10,11]])


def test_non_divisible():
    _test_batched(range(10), n=3, expected=[[0,1,2], [3,4,5], [6,7,8], [9]])


def _test_batched(iterable, n, expected):
    fillvalue = object()

    for actual_batch, expected_batch in zip_longest(batched(iterable, n), expected, fillvalue=fillvalue):
        if actual_batch is fillvalue or expected_batch is fillvalue:
            raise TypeError()

        for actual_item, expected_item in zip_longest(actual_batch, expected_batch, fillvalue=fillvalue):
            if actual_item is fillvalue or expected_item is fillvalue:
                raise TypeError()

            assert actual_item == expected_item
