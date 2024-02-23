from typing import Iterable, Optional, Callable, Generator, TypeVar, Any, Union, Union, List
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor, Executor, Future
from contextlib import contextmanager
from functools import partial
import time

from typing_extensions import Literal
from tqdm import tqdm, trange


T = TypeVar('T')
R = TypeVar('R')


def with_progbar(iterable: Union[Iterable[T], int], postfix_fn: Optional[Callable[[T], Any]] = None, **kwargs) -> Generator[T, None, None]:
    if isinstance(iterable, int):
        tqdm_iter = trange(iterable, **kwargs)
    else:
        tqdm_iter = tqdm(iterable, **kwargs)

    for item in tqdm_iter:
        if postfix_fn is not None:
            tqdm_iter.set_postfix_str(str(postfix_fn(item)))

        yield item


def with_async_progbar(iterable: Iterable[T], worker: Callable[[T], R], *, max_workers: Optional[int] = None, postfix_fn: Optional[Callable[[R], Any]] = None, unpack_into_worker: bool, **kwargs) -> Generator[R, None, None]:
    with tqdm(**kwargs) as pbar:
        with ThreadPoolExecutor(max_workers) as executor:
            for future in as_completed(executor.submit(worker, *item if unpack_into_worker else item) for item in iterable):
                item = future.result()
                pbar.update()

                if postfix_fn is not None:
                    pbar.set_postfix_str(str(postfix_fn(item)), refresh=False)

                pbar.refresh()
                e = future.exception()

                if e:
                    raise e

                yield item


def exhaust(iterable: Iterable) -> None:
    for _ in iterable:
        pass


class _DummyContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _make_progbar_updater(postfix_fn):
    def set_postfix_str(progbar: tqdm, result):
        progbar.set_postfix_str(str(postfix_fn(result)))

    return set_postfix_str


class _DummyFuture:
    _NONE = object()

    def __init__(self, func, value):
        self._func = func
        self._value = value
        self._result = self._NONE

    def result(self):
        if self._result is self._NONE:
            self._result = self._func(self._value)
        
        return self._result

    def exception(self):
        if self._result is self._NONE:
            self._result = self._func(self._value)

        return None


class _DummyExecutor(_DummyContext):
    def submit(self, fn, item):
        return _DummyFuture(fn, item)
    

class _DummyProgbar(_DummyContext):
    def __call__(self, outputs):
        pass


class TqdmProgbar:
    def __init__(self, postfix_str: Optional[Union[str, Callable[[Any], Any]]] = None, **kwargs):
        self._tqdm = tqdm(**kwargs)

        if isinstance(postfix_str, str):
            self._tqdm.set_postfix_str(postfix_str)
        elif callable(postfix_str):
            self._progbar_on_advance = _make_progbar_updater(postfix_str)

    def __enter__(self):
        self._tqdm.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tqdm.__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, outputs):
        self._tqdm.update()
        self._progbar_on_advance(self._tqdm, outputs)
        self._tqdm.refresh()


class ResultPacker:
    __slots__ = ('inputs', 'outputs', 'enumerations')

    def __init__(self, inputs: bool = False, outputs: bool = True, enumerations: bool = False):
        self.inputs = inputs
        self.outputs = outputs
        self.enumerations = enumerations

    def __call__(self, inputs, outputs, enumeration):
        if (not self.inputs) and (not self.outputs) and (not self.enumerations):  # 000
            return None
        elif (not self.inputs) and (not self.outputs) and (self.enumerations):  # 001
            return enumeration
        elif (not self.inputs) and (self.outputs) and (not self.enumerations):  # 010
            return outputs
        elif (not self.inputs) and (self.outputs) and (self.enumerations):  # 011
            return enumeration, outputs
        elif (self.inputs) and (not self.outputs) and (not self.enumerations):  # 100
            return self.inputs
        elif (self.inputs) and (not self.outputs) and (self.enumerations):  # 101
            return enumeration, inputs
        elif (self.inputs) and (self.outputs) and (not self.enumerations):  # 110
            return inputs, outputs
        else:  # 111
            return enumeration, inputs, outputs


class Apply:
    def __init__(self) -> None:
        self._progbar = _DummyProgbar()
        self._total = None
        self._function = self._function_args = None
        self._iterable = None
        self._delay = 0.0
        self._executor: Executor = _DummyExecutor()
        self._result_packer = ResultPacker()

    @classmethod
    def function(cls, fn, *args, **kwargs) -> 'Apply':
        self = cls()
        self._function = partial(fn, *args, **kwargs)

        return self
    
    def to(self, iterable) -> 'Apply':
        self._iterable = iterable

        return self

    def with_progbar(self, total: Optional[Union[str, Callable[[Any], int]]] = None, postfix_str: Optional[Union[str, Callable[[Any], Any]]] = None, **kwargs) -> 'Apply':
        if callable(total):
            kwargs['total'] = total(self._iterable)

        self._progbar = TqdmProgbar(postfix_str, **kwargs)

        return self

    def concurrently(self, how: Literal['multi-processing', 'multi-threading'], max_workers: Optional[int] = None) -> 'Apply':
        if how == 'multi-threading':
            self._executor = ThreadPoolExecutor(max_workers)
        else:
            self._executor = ProcessPoolExecutor(max_workers)

        return self
    
    def delay(self, seconds: float) -> 'Apply':
        self._delay = seconds

        return self

    def returning(self, inputs: bool = False, outputs: bool = True, enumerations: bool = False) -> 'Apply':
        self._result_packer = ResultPacker(inputs, outputs, enumerations)

        return self

    def exhaust(self) -> None:
        for _ in self:
            pass

    def __iter__(self):
        with self._progbar as progbar:
            with self._executor as executor:
                futures: List[Future] = []
                inputs = []

                for item in self._iterable:
                    futures.append(executor.submit(self._function, item))

                    if self._result_packer.inputs:
                        inputs.append(item)
                    else:
                        inputs.append(None)

                for i, (input_, future) in enumerate(zip(inputs, futures)):
                    exception = future.exception()

                    if exception:
                        raise exception

                    output = future.result()
                    progbar(output)

                    yield self._result_packer(input_, output, i)

                    if self._delay:
                        time.sleep(self._delay)


if __name__ == '__main__':
    import math
    numbers = list(range(100))

    def func(x):
        time.sleep(1)
        return x ** 2

    # for _ in Apply.function(func).to(numbers).with_progbar(total=len, desc='Square', postfix_str=str).returning(inputs=True, outputs=True, enumerations=False).concurrently('multi-processing'):
    #     print(_)

    Apply.function(func).to(numbers).delay(0.1).with_progbar(total=len, desc='Square', postfix_str=str).concurrently('multi-processing', max_workers=5).exhaust()
