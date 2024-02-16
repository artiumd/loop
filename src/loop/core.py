from typing import Iterable, Iterator, TypeVar, Literal, Tuple, Dict, Optional
from functools import reduce

from .functional import args_last_adapter, args_first_adapter, tuple_unpack_args_last_adapter, tuple_unpack_args_first_adapter, dict_unpack_adapter, filter_adapter, skipped


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
        for inp in self._iterable:
            out = inp

            for function in self._functions:
                out = function(out)

                if out is skipped:
                    break
            else:
                yield out

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
