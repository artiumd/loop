from threading import get_ident
from os import getpid
import time

import pytest

from src.loop import loop_over


def test_different_thread_ids():
    def wait_and_get_id(x):
        time.sleep(0.01)
        return get_ident()

    num_threads = 7
    loop = loop_over(range(100)).map(wait_and_get_id).concurrently('threads', num_workers=num_threads)
    unique_ids = set(loop)
    assert len(unique_ids) == num_threads


def test_disabled_threads():
    main_id = get_ident()

    def assert_in_main_thread(x):
        time.sleep(0.01)
        assert get_ident() == main_id

    loop_over(range(100)).map(assert_in_main_thread).concurrently('processes', num_workers=0).exhaust()


def test_same_process_id():
    main_id = getpid()

    def wait_and_get_id(x):
        time.sleep(0.01)
        return getpid()

    loop = loop_over(range(100)).map(wait_and_get_id).concurrently('threads')
    unique_ids = set(loop)
    assert len(unique_ids) == 1
    assert list(unique_ids)[0] == main_id


def test_different_process_ids():
    def wait_and_get_id(x):
        time.sleep(0.01)
        return getpid()

    num_processes = 7
    loop = loop_over(range(100)).map(wait_and_get_id).concurrently('processes', num_workers=num_processes)
    unique_ids = set(loop)
    assert len(unique_ids) == num_processes


def test_disabled_processes():
    main_id = getpid()

    def assert_in_main_thread(x):
        time.sleep(0.01)
        assert getpid() == main_id

    loop_over(range(100)).map(assert_in_main_thread).concurrently('processes', num_workers=0).exhaust()


def test_raise_errors_in_threads():
    def raise_error(x):
        raise TypeError(x)

    with pytest.raises(TypeError):
        loop_over(range(100)).map(raise_error).concurrently('threads').exhaust()


def test_return_errors_in_threads():
    def raise_error(x):
        raise TypeError(x)

    for x in loop_over(range(100)).map(raise_error).concurrently('threads', exceptions='return'):
        assert isinstance(x, TypeError)


def test_raise_errors_in_processes():
    def raise_error(x):
        raise TypeError(x)

    with pytest.raises(TypeError):
        loop_over(range(100)).map(raise_error).concurrently('processes').exhaust()


def test_return_errors_in_processes():
    def raise_error(x):
        raise TypeError(x)

    for x in loop_over(range(100)).map(raise_error).concurrently('processes', exceptions='return'):
        assert isinstance(x, TypeError)
