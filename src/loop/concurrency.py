from typing import Callable, TypeVar


T = TypeVar('T')
R = TypeVar('R')


class _DummyFuture:
    def __init__(self, func: Callable[[T], R], inp: T):
        self._func = func
        self._inp = inp
        self._result = None
        self._exception = None
        self._ready = False

    def result(self) -> R:
        self._compute()
        return self._result

    def _compute(self) -> None:
        if self._ready:
            return

        self._result = self._func(self._inp)
        self._ready = True


class DummyExecutor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def submit(self, fn, item):
        return _DummyFuture(fn, item)