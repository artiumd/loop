from typing import Iterable, Iterator, TypeVar, Literal, Tuple, Dict, Optional, Union, Callable, Any
from functools import reduce

from .functional import args_last_adapter, args_first_adapter, tuple_unpack_args_last_adapter, tuple_unpack_args_first_adapter, dict_unpack_adapter, filter_adapter, skipped
from .packing import return_first, return_first_and_second, return_first_and_third, return_first_second_and_third, return_second, return_second_and_third, return_third, return_none
from .progress import dummy_progress, TqdmProgbar


T = TypeVar('T')
A = TypeVar('A')
K = TypeVar('K')
R = TypeVar('R')


_missing = object()


class Loop:
    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable
        self._functions = []
        self._next_call_spec: Tuple[Optional[Literal['*', '**']], bool] = (None, False)

        self._retval_packer = return_third
        self._returning_inputs = False
        self._returning_outputs = True

        self._progbar = dummy_progress()

    def next_call_with(self, unpacking: Optional[Literal['*', '**']] = None, args_first: bool = False) -> 'Loop':
        """
        Change how arguments are passed to `function` in [`map()`][loop.Loop.map] (or `predicate` in [`filter()`][loop.Loop.filter]).

        Arguments are explained using the following table:

        | `unpacking` | `args_first` | Resulting Call                                                 |
        |-------------|--------------|-----------------------------------------------------------------
        |    `None`   |    `False`   | `func(x, *args, **kwargs)` (this is the default behaviour)     |
        |    `None`   |    `True`    | `func(*args, x, **kwargs)`                                     |
        |    `"*"`    |    `False`   | `func(*x, *args, **kwargs)`                                    |
        |    `"*"`    |    `True`    | `func(*args, *x, **kwargs)`                                    |
        |    `"**"`   |    `Any`     | `func(*args, **x, **kwargs)`                                   |

        Returns:
            Returns `self` to allow for further method chaining.

        !!! note

            Each invocation of `next_call_with()` applies only to the next `map()`/`filter()`, subsequent calls will resume to default behaviour.
        """
        self._next_call_spec = (unpacking, args_first)
        return self

    def map(self, function, *args: A, **kwargs: K) -> 'Loop':
        """
        Apply `function` to each `item` in `iterable` by calling `function(item, *args, **kwargs)`.

        Example:
            --8<-- "docs/examples/map_single.md"

        Args:
            function: Function to be applied on each item in the loop.
            args: Passed as `*args` (after the loop variable) to each call to `function`.
            kwargs: Passed as `**kwargs` to each call to `function`.

        Returns:
            Returns `self` to allow for further method chaining.

        !!! note

            By default, applying ` map(function, *args, **kwargs)` is not the same as applying `map(functools.partial(function, *args, **kwargs))` because `functools.partial` passes `*args` BEFORE the loop item.
        """
        self._set_map_or_filter(function, args, kwargs, filtering=False)
        return self

    def filter(self, predicate, *args: A, **kwargs: K) -> 'Loop':
        """
        Skip items for which `predicate(item, *args, **kwargs)` is false.

        Example:
            ``` python

            from loop import loop_over


            for number in loop_over(range(10)).filter(lambda x: x%2==0):
                print(number)
            ```

            ``` console
            0
            2
            4
            6
            8
            ```
        
        Args:
            predicate: Function that accepts the loop variable and returns a boolean.
            args: Passed as `*args` (after the loop variable) to each call to `predicate`.
            kwargs: Passed as `**kwargs` to each call to `predicate`.

        Returns:
            Returns `self` to allow for further method chaining.
        """
        self._set_map_or_filter(predicate, args, kwargs, filtering=True)
        return self
    
    def returning(self, enumerations: bool = False, inputs: bool = False, outputs: bool = True) -> 'Loop':
        """
        Set the return type of this loop.

        By default, only outputs are returned.

        The order of returned items is `(enumerations, inputs, outputs)`.

        Example:
            ``` python

            from loop import loop_over


            for retval in loop_over(range(0, 10, 2)).map(pow, 2).returning(enumerations=True, inputs=True, outputs=True):
                print(retval)
            ```

            ``` console
            (0, 0, 0) 
            (1, 2, 4) 
            (2, 4, 16)
            (3, 6, 36)
            (4, 8, 64)
            ```

        Args:
            enumerations: If True, return value will include the (zero-based) index of the current iteration.
            inputs: If True, return value will include the raw value from the underlying iterable, before any [`map()`][loop.Loop.map] has been applied.
            outputs: If True, return value will include the output of the last [`map()`][loop.Loop.map] operation.

        Returns:
            Returns `self` to allow for further method chaining.
        """
        if not enumerations and not inputs and not outputs:  # 000
            self._retval_packer = return_none
        elif not enumerations and not inputs and outputs:  # 001
            self._retval_packer = return_third
        elif not enumerations and inputs and not outputs:  # 010
            self._retval_packer = return_second
        elif not enumerations and inputs and outputs:  # 011
            self._retval_packer = return_second_and_third
        elif enumerations and not inputs and not outputs:  # 100
            self._retval_packer = return_first
        elif enumerations and not inputs and outputs:  # 101
            self._retval_packer = return_first_and_third
        elif enumerations and inputs and not outputs:  # 110
            self._retval_packer = return_first_and_second
        elif enumerations and inputs and outputs:  # 111
            self._retval_packer = return_first_second_and_third

        self._returning_inputs = inputs
        self._returning_outputs = outputs

        return self

    def show_progress(self, postfix_str: Optional[Union[str, Callable[[Any], Any]]] = None, total: Optional[Union[int, Callable[[Iterable], int]]] = None, **kwargs) -> 'Loop':
        if callable(total):
            total = total(self._iterable)

        self._progbar = TqdmProgbar(postfix_str=postfix_str, total=total, **kwargs)
        return self

    def exhaust(self) -> None:
        """
        Consume the loop without returning any results.

        This maybe useful when you map functions only for their side effects.

        Example:
            ```python
            from loop import loop_over


            items = []
            loop_over(range(5)).map(items.append).exhaust()
            print(items)
            ```
            ```console
            [0, 1, 2, 3, 4]
            ```
        """
        for _ in self:
            pass

    def reduce(self, function, initializer=_missing):
        """
        Consume the loop and reduce it to a single value using `function`.

        `function` and (the optional) `initializer` have the same 
        meaning as in [`functools.reduce()`](https://docs.python.org/3/library/functools.html#functools.reduce).

        Example:
            ```python
            from loop import loop_over


            vec = [-1.1, 25.3, 4.9]
            sum_squares = loop_over(vec).map(lambda x: x**2).reduce(lambda x,y: x+y)
            print(f'The L2 norm of {vec} equals {sum_squares**0.5:.2f}')
            ```
            ```console
            The L2 norm of [-1.1, 25.3, 4.9] equals 25.79
            ```
        """
        if initializer is _missing:
            initializer = ()
        else:
            initializer = (initializer, )

        return reduce(function, self, *initializer)

    def __iter__(self) -> Iterator[R]:
        """
        The most common way to consume a loop is to simply iterate over it.

        Example:
            ```python
            from loop import loop_over


            items = ...

            for item in loop_over(items):
                # Do something with item
                pass
            ```
        """
        with self._progbar as progbar:
            for i, inp in enumerate(self._iterable):
                out = inp

                for function in self._functions:
                    out = function(out)

                    if out is skipped:
                        break
                else:
                    retval = self._retval_packer(i, inp, out)
                    progbar(retval)

                    yield retval

    def _set_map_or_filter(self, function, args: Tuple[A, ...], kwargs: Dict[str, K], filtering: bool) -> None:
        unpacking, args_first = self._next_call_spec
        self._next_call_spec = (None, False)

        if unpacking == '**':
            adapter = dict_unpack_adapter
        elif unpacking == '*':
            if args_first:
                adapter = tuple_unpack_args_first_adapter
            else:
                adapter = tuple_unpack_args_last_adapter
        else:
            if args_first:
                adapter = args_first_adapter
            else:
                adapter = args_last_adapter

        function = adapter(function, *args, **kwargs)

        if filtering:
            function = filter_adapter(function)

        self._functions.append(function)


def loop_over(iterable: Iterable[T]) -> Loop:
    """Construct a new `Loop`.

    Customize the looping behaviour by chaining different `Loop` methods and finally use a `for` statement like you normally would.

    Example:
        --8<-- "docs/examples/minimal.md"

    Args:
        iterable: The object to be looped over.

    Returns:
        Returns a new `Loop` instance wrapping `iterable`.
    """
    return Loop(iterable)
