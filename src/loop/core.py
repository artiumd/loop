from typing import Iterable, Iterator, TypeVar, Protocol
from functools import reduce


T = TypeVar('T')
A = TypeVar('A')
K = TypeVar('K')
R = TypeVar('R')


_missing = object()


class Function(Protocol):
    def __call__(self, *args: A, **kwargs: K) -> R:
        ...


class Mapper:
    __slots__ = ('_args', '_kwargs', '_function')

    def __init__(self, function: Function, *args: A, **kwargs: K):
        self._args = args
        self._kwargs = kwargs
        self._function = function

    def __call__(self, inp: T) -> R:
        return self._function(inp, *self._args, **self._kwargs)


class UnpackerMapper(Mapper):
    __slots__ = ()

    def __call__(self, inp: T) -> R:
        return self._function(*inp, *self._args, **self._kwargs)


class Loop:
    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable
        self._mappers = []

    def map(self, function: Function, *args: A, **kwargs: K) -> 'Loop':
        """
        Apply `function` to each `item` in `iterable` by calling `function(item, *args, **kwargs)`.

        Example:
            --8<-- "docs/examples/map_single.md"

        Args:
            function: Function to be applied on each item in the loop.
            args: Passed as `*args` (after the loop item) to each call to `function`.
            kwargs: Passed as `**kwargs` to each call to `function`.

        Returns:
            Returns `self` to allow for further method chaining.

        !!! note

            Applying ` map(function, *args, **kwargs)` is not the same as applying `map(functools.partial(function, *args, **kwargs))` because `functools.partial` passes `*args` BEFORE the loop item.
        """
        self._mappers.append(Mapper(function, *args, **kwargs))
        return self

    def unpack_map(self, function: Function, *args: A, **kwargs: K) -> 'Loop':
        """
        This is the same as [`map()`][loop.Loop.map] except that the `item` from `iterable` is star unpacked as it is passed to `function` i.e. `function(*item, *args, **kwargs)`.
        
        Example:
            ``` python
            from pathlib import Path

            from loop import loop_over


            def touch(root, *parts, name):
                path = Path(root).joinpath(*parts, name)
                path.parent.mkdir(exist_ok=True, parents=True)
                path.joinpath(name).touch()
                return str(path)

                
            paths = [['/tmp', 'foo'], 
                     ['/home', 'user', 'bar'], 
                     ['/var', 'log.txt']]

     
            for path in loop_over(paths).unpack_map(touch):
                print(f'Created {path}')
            ```

            ``` console
            Created /tmp/foo
            Created /home/user/bar
            Created /var/log.txt
            ```
        """
        self._mappers.append(UnpackerMapper(function, *args, **kwargs))
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

            for mapper in self._mappers:
                out = mapper(out)

            yield out


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
