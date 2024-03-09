from typing import List, Dict, Tuple
from operator import add

from src.loop import loop_range, loop_over


def test_simple() -> None:
    x: int
    for x in loop_range(10): pass
    for x in loop_over(range(10)): pass

    y: str
    for y in loop_over('hello world'): pass


def test_map() -> None:
    x: List[int]
    for x in loop_range(10).map(lambda x: [x]): pass

    y: Dict[str, str]
    for y in loop_over([1.1, 2.2, 3.3]).map(str).map(lambda x: {x: x}): pass


def test_filter() -> None:
    x: int
    for x in loop_range(10).filter(lambda x: x > 5): pass


def test_returning_after_map() -> None:
    inp = ['hello', 'world']

    def func(word: str) -> float:
        return sum(char == 'l' for char in word) / len(word)

    def test_none() -> None:
        x: None
        for x in loop_over(inp).map(func).returning(outputs=False): pass
        for x in loop_over(inp).map(func).returning(inputs=False, outputs=False): pass
        for x in loop_over(inp).map(func).returning(False, outputs=False): pass
        for x in loop_over(inp).map(func).returning(False, False, False): pass
        for x in loop_over(inp).map(func).returning(False, False, outputs=False): pass
        for x in loop_over(inp).map(func).returning(False, inputs=False, outputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, outputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, inputs=False, outputs=False): pass

    def test_outputs_only() -> None:
        x: float
        for x in loop_over(inp).map(func).returning(): pass
        for x in loop_over(inp).map(func).returning(outputs=True): pass
        for x in loop_over(inp).map(func).returning(inputs=False): pass
        for x in loop_over(inp).map(func).returning(inputs=False, outputs=True): pass
        for x in loop_over(inp).map(func).returning(False): pass
        for x in loop_over(inp).map(func).returning(False, outputs=True): pass
        for x in loop_over(inp).map(func).returning(False, False): pass
        for x in loop_over(inp).map(func).returning(False, False, True): pass
        for x in loop_over(inp).map(func).returning(False, False, outputs=True): pass
        for x in loop_over(inp).map(func).returning(False, inputs=False): pass
        for x in loop_over(inp).map(func).returning(False, inputs=False, outputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, outputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, inputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, inputs=False, outputs=True): pass

    def test_inputs_outputs() -> None:
        x: Tuple[str, float]
        for x in loop_over(inp).map(func).returning(inputs=True): pass
        for x in loop_over(inp).map(func).returning(inputs=True, outputs=True): pass
        for x in loop_over(inp).map(func).returning(False, True): pass
        for x in loop_over(inp).map(func).returning(False, True, True): pass
        for x in loop_over(inp).map(func).returning(False, True, outputs=True): pass
        for x in loop_over(inp).map(func).returning(False, inputs=True): pass
        for x in loop_over(inp).map(func).returning(False, inputs=True, outputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, inputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, inputs=True, outputs=True): pass

    def test_inputs_only() -> None:
        x: str
        for x in loop_over(inp).map(func).returning(inputs=True, outputs=False): pass
        for x in loop_over(inp).map(func).returning(False, True, False): pass
        for x in loop_over(inp).map(func).returning(False, True, outputs=False): pass
        for x in loop_over(inp).map(func).returning(False, inputs=True, outputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=False, inputs=True, outputs=False): pass

    def test_enums_outputs() -> None:
        x: Tuple[int, float]
        for x in loop_over(inp).map(func).returning(True): pass
        for x in loop_over(inp).map(func).returning(True, outputs=True): pass
        for x in loop_over(inp).map(func).returning(True, False): pass
        for x in loop_over(inp).map(func).returning(True, False, True): pass
        for x in loop_over(inp).map(func).returning(True, False, outputs=True): pass
        for x in loop_over(inp).map(func).returning(True, inputs=False): pass
        for x in loop_over(inp).map(func).returning(True, inputs=False, outputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, outputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, inputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, inputs=False, outputs=True): pass

    def test_enums_only() -> None:
        x: int
        for x in loop_over(inp).map(func).returning(True, outputs=False): pass
        for x in loop_over(inp).map(func).returning(True, False, False): pass
        for x in loop_over(inp).map(func).returning(True, False, outputs=False): pass
        for x in loop_over(inp).map(func).returning(True, inputs=False, outputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, outputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, inputs=False, outputs=False): pass

    def test_enums_inputs_outputs() -> None:
        x: Tuple[int, str, float]
        for x in loop_over(inp).map(func).returning(True, True): pass
        for x in loop_over(inp).map(func).returning(True, True, True): pass
        for x in loop_over(inp).map(func).returning(True, True, outputs=True): pass
        for x in loop_over(inp).map(func).returning(True, inputs=True): pass
        for x in loop_over(inp).map(func).returning(True, inputs=True, outputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, inputs=True): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, inputs=True, outputs=True): pass

    def test_enums_inputs() -> None:
        x: Tuple[int, str]
        for x in loop_over(inp).map(func).returning(True, True, False): pass
        for x in loop_over(inp).map(func).returning(True, True, outputs=False): pass
        for x in loop_over(inp).map(func).returning(True, inputs=True, outputs=False): pass
        for x in loop_over(inp).map(func).returning(enumerations=True, inputs=True, outputs=False): pass


def test_returning_before_map() -> None:
    inp = ['hello', 'world']

    def func(word: str) -> float:
        return sum(char == 'l' for char in word) / len(word)

    def test_none() -> None:
        x: None
        for x in loop_over(inp).returning(outputs=False).map(func): pass
        for x in loop_over(inp).returning(inputs=False, outputs=False).map(func): pass
        for x in loop_over(inp).returning(False, outputs=False).map(func): pass
        for x in loop_over(inp).returning(False, False, False).map(func): pass
        for x in loop_over(inp).returning(False, False, outputs=False).map(func): pass
        for x in loop_over(inp).returning(False, inputs=False, outputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, outputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, inputs=False, outputs=False).map(func): pass

    def test_outputs_only() -> None:
        x: float
        for x in loop_over(inp).returning().map(func): pass
        for x in loop_over(inp).returning(outputs=True).map(func): pass
        for x in loop_over(inp).returning(inputs=False).map(func): pass
        for x in loop_over(inp).returning(inputs=False, outputs=True).map(func): pass
        for x in loop_over(inp).returning(False).map(func): pass
        for x in loop_over(inp).returning(False, outputs=True).map(func): pass
        for x in loop_over(inp).returning(False, False).map(func): pass
        for x in loop_over(inp).returning(False, False, True).map(func): pass
        for x in loop_over(inp).returning(False, False, outputs=True).map(func): pass
        for x in loop_over(inp).returning(False, inputs=False).map(func): pass
        for x in loop_over(inp).returning(False, inputs=False, outputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, outputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, inputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, inputs=False, outputs=True).map(func): pass

    def test_inputs_outputs() -> None:
        x: Tuple[str, float]
        for x in loop_over(inp).returning(inputs=True).map(func): pass
        for x in loop_over(inp).returning(inputs=True, outputs=True).map(func): pass
        for x in loop_over(inp).returning(False, True).map(func): pass
        for x in loop_over(inp).returning(False, True, True).map(func): pass
        for x in loop_over(inp).returning(False, True, outputs=True).map(func): pass
        for x in loop_over(inp).returning(False, inputs=True).map(func): pass
        for x in loop_over(inp).returning(False, inputs=True, outputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, inputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, inputs=True, outputs=True).map(func): pass

    def test_inputs_only() -> None:
        x: str
        for x in loop_over(inp).returning(inputs=True, outputs=False).map(func): pass
        for x in loop_over(inp).returning(False, True, False).map(func): pass
        for x in loop_over(inp).returning(False, True, outputs=False).map(func): pass
        for x in loop_over(inp).returning(False, inputs=True, outputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=False, inputs=True, outputs=False).map(func): pass

    def test_enums_outputs() -> None:
        x: Tuple[int, float]
        for x in loop_over(inp).returning(True).map(func): pass
        for x in loop_over(inp).returning(True, outputs=True).map(func): pass
        for x in loop_over(inp).returning(True, False).map(func): pass
        for x in loop_over(inp).returning(True, False, True).map(func): pass
        for x in loop_over(inp).returning(True, False, outputs=True).map(func): pass
        for x in loop_over(inp).returning(True, inputs=False).map(func): pass
        for x in loop_over(inp).returning(True, inputs=False, outputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, outputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, inputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, inputs=False, outputs=True).map(func): pass

    def test_enums_only() -> None:
        x: int
        for x in loop_over(inp).returning(True, outputs=False).map(func): pass
        for x in loop_over(inp).returning(True, False, False).map(func): pass
        for x in loop_over(inp).returning(True, False, outputs=False).map(func): pass
        for x in loop_over(inp).returning(True, inputs=False, outputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, outputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, inputs=False, outputs=False).map(func): pass

    def test_enums_inputs_outputs() -> None:
        x: Tuple[int, str, float]
        for x in loop_over(inp).returning(True, True).map(func): pass
        for x in loop_over(inp).returning(True, True, True).map(func): pass
        for x in loop_over(inp).returning(True, True, outputs=True).map(func): pass
        for x in loop_over(inp).returning(True, inputs=True).map(func): pass
        for x in loop_over(inp).returning(True, inputs=True, outputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, inputs=True).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, inputs=True, outputs=True).map(func): pass

    def test_enums_inputs() -> None:
        x: Tuple[int, str]
        for x in loop_over(inp).returning(True, True, False).map(func): pass
        for x in loop_over(inp).returning(True, True, outputs=False).map(func): pass
        for x in loop_over(inp).returning(True, inputs=True, outputs=False).map(func): pass
        for x in loop_over(inp).returning(enumerations=True, inputs=True, outputs=False).map(func): pass


def test_reduce() -> None:
    inp = [1.1, 2.2, 3.3, 4.4, 5.5]
    a: float = loop_over(inp).reduce(add)
    b: str = loop_over(inp).map(str).reduce(add)
    c: float = loop_over(inp).map(str).returning(inputs=True, outputs=False).reduce(add)
    d: Tuple[float, str] = loop_over(inp).map(str).returning(inputs=True).reduce(add)
    e: int = loop_over(inp).map(str).returning(enumerations=True, outputs=False).reduce(add)
    f: Tuple[int, str] = loop_over(inp).map(str).returning(enumerations=True).reduce(add)
    g: Tuple[int, float] = loop_over(inp).map(str).returning(enumerations=True, inputs=True, outputs=False).reduce(add)
    h: Tuple[int, float, str] = loop_over(inp).map(str).returning(enumerations=True, inputs=True).reduce(add)
