![tests](https://github.com/artiumd/loop/actions/workflows/tests.yml/badge.svg)

# Welcome to `loop`

Replace common looping boilerplate with pretty method chaining.

## Installation

``` bash

pip install loop-python
```

## Documentation 

Visit the [documentation site](https://artiumd.github.io/loop/latest/).

## Example

Loop over `range(20)`, apply the `fibo()` function and then, on top of it, apply the `fizzbuzz()` function, finally, apply `print()`:

``` python
from loop import loop_over


def fizzbuzz(x):
    rules = {3: 'fizz', 5: 'buzz'}.items()
    res = ''.join(word for div, word in rules if x%div == 0)
    return res if res else x


def fibo(x):
    a, b = 1, 1
    for _ in range(1, x):
        a, b = b, a + b
    return b


loop_over(range(20)).map(fibo).map(fizzbuzz).map(print).exhaust()
```

Will produce the following output:

``` console
1
1
2
fizz
buzz
8
13
fizz
34
buzz
89
fizz
233
377
buzz
fizz
1597
2584
4181
fizzbuzz
```
