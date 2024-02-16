## Minimal Working Example

At its core, `loop` provides wrappers around iterables (to which we can add some enhancements).

--8<-- "docs/examples/minimal.md"

## Mapping Functions To Loops

Using the `map()` method we can apply a function to each of the iterable:

--8<-- "docs/examples/map_single.md"

### Chaining And Ordering Of `*args`

Furthermore, we can chain multiple `map()`s together and provide additional arguments to each function.

In this example, we compute the 5 first powers of π, rounded to two decimal places:

``` python

from math import pi

from loop import loop_over


for x in loop_over(range(5)).next_call_with(args_first=True).map(pow, pi).map(round, 2):
    print(x)
```

``` console
1.0
3.14
9.87
31.01
97.41
```

As we can see in the second call to `map()`, we can pass additional positional (and named) arguments that will be added after the loop variable (in this case, `round(x, 2)` will be called).

The additional positional arguments are passed (by default) after the loop variable, which by default would cause `map(pow, pi)` to call `pow(x, pi)` instead of `pow(pi, x)`. We can modify the calling format to fit our needs by preceeding `map(pow, pi)` with `next_call_with(args_first=True)`.

### Argument Unpacking

The loop variable is naturally a single object, but what if your function expects multiple arguments?

Again, `next_call_with()` can solve this problem. In the following example, we convert 4 complex numbers from cartesian to polar representation (in degrees).

``` python

from math import degrees
from cmath import polar

from loop import loop_over


polars = (loop_over([(1,0),(0,1),(-1,0),(0,-1)]).
          next_call_with(unpack='*').
          map(complex).
          map(polar).
          next_call_with(unpack='*').
          map(lambda r,t: (r, degrees(t))))

for x in polars:
    print(x)
```

``` console
(1.0, 0.0)
(1.0, 90.0)
(1.0, 180.0)
(1.0, -90.0)
```
