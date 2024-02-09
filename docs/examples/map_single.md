``` python

from loop import loop_over


for word in loop_over(['Hello', 'World', '!']).map(lambda s: s.upper()):
    print(word)
```

``` console
HELLO
WORLD
!
```