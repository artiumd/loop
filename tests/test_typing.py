from typing import List, Dict, Tuple
from operator import add

from src.loop import loop_range, loop_over, Loop, TRUE, FALSE


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
    def _calc_l_rate(word: str) -> float:
        return sum(char == 'l' for char in word) / len(word)

    def _make_loop() -> Loop[str, float, FALSE, FALSE, TRUE]:
        return loop_over(['hello', 'world']).map(_calc_l_rate)

    def test_none() -> None:
        x: None
        for x in _make_loop().returning(outputs=False): pass
        for x in _make_loop().returning(inputs=False, outputs=False): pass
        for x in _make_loop().returning(False, outputs=False): pass
        for x in _make_loop().returning(False, False, False): pass
        for x in _make_loop().returning(False, False, outputs=False): pass
        for x in _make_loop().returning(False, inputs=False, outputs=False): pass
        for x in _make_loop().returning(enumerations=False, outputs=False): pass
        for x in _make_loop().returning(enumerations=False, inputs=False, outputs=False): pass

    def test_outputs_only() -> None:
        x: float
        for x in _make_loop().returning(): pass
        for x in _make_loop().returning(outputs=True): pass
        for x in _make_loop().returning(inputs=False): pass
        for x in _make_loop().returning(inputs=False, outputs=True): pass
        for x in _make_loop().returning(False): pass
        for x in _make_loop().returning(False, outputs=True): pass
        for x in _make_loop().returning(False, False): pass
        for x in _make_loop().returning(False, False, True): pass
        for x in _make_loop().returning(False, False, outputs=True): pass
        for x in _make_loop().returning(False, inputs=False): pass
        for x in _make_loop().returning(False, inputs=False, outputs=True): pass
        for x in _make_loop().returning(enumerations=False): pass
        for x in _make_loop().returning(enumerations=False, outputs=True): pass
        for x in _make_loop().returning(enumerations=False, inputs=False): pass
        for x in _make_loop().returning(enumerations=False, inputs=False, outputs=True): pass

    def test_inputs_outputs() -> None:
        x: Tuple[str, float]
        for x in _make_loop().returning(inputs=True): pass
        for x in _make_loop().returning(inputs=True, outputs=True): pass
        for x in _make_loop().returning(False, True): pass
        for x in _make_loop().returning(False, True, True): pass
        for x in _make_loop().returning(False, True, outputs=True): pass
        for x in _make_loop().returning(False, inputs=True): pass
        for x in _make_loop().returning(False, inputs=True, outputs=True): pass
        for x in _make_loop().returning(enumerations=False, inputs=True): pass
        for x in _make_loop().returning(enumerations=False, inputs=True, outputs=True): pass

    def test_inputs_only() -> None:
        x: str
        for x in _make_loop().returning(inputs=True, outputs=False): pass
        for x in _make_loop().returning(False, True, False): pass
        for x in _make_loop().returning(False, True, outputs=False): pass
        for x in _make_loop().returning(False, inputs=True, outputs=False): pass
        for x in _make_loop().returning(enumerations=False, inputs=True, outputs=False): pass

    def test_enums_outputs() -> None:
        x: Tuple[int, float]
        for x in _make_loop().returning(True): pass
        for x in _make_loop().returning(True, outputs=True): pass
        for x in _make_loop().returning(True, False): pass
        for x in _make_loop().returning(True, False, True): pass
        for x in _make_loop().returning(True, False, outputs=True): pass
        for x in _make_loop().returning(True, inputs=False): pass
        for x in _make_loop().returning(True, inputs=False, outputs=True): pass
        for x in _make_loop().returning(enumerations=True): pass
        for x in _make_loop().returning(enumerations=True, outputs=True): pass
        for x in _make_loop().returning(enumerations=True, inputs=False): pass
        for x in _make_loop().returning(enumerations=True, inputs=False, outputs=True): pass

    def test_enums_only() -> None:
        x: int
        for x in _make_loop().returning(True, outputs=False): pass
        for x in _make_loop().returning(True, False, False): pass
        for x in _make_loop().returning(True, False, outputs=False): pass
        for x in _make_loop().returning(True, inputs=False, outputs=False): pass
        for x in _make_loop().returning(enumerations=True, outputs=False): pass
        for x in _make_loop().returning(enumerations=True, inputs=False, outputs=False): pass

    def test_enums_inputs_outputs() -> None:
        x: Tuple[int, str, float]
        for x in _make_loop().returning(True, True): pass
        for x in _make_loop().returning(True, True, True): pass
        for x in _make_loop().returning(True, True, outputs=True): pass
        for x in _make_loop().returning(True, inputs=True): pass
        for x in _make_loop().returning(True, inputs=True, outputs=True): pass
        for x in _make_loop().returning(enumerations=True, inputs=True): pass
        for x in _make_loop().returning(enumerations=True, inputs=True, outputs=True): pass

    def test_enums_inputs() -> None:
        x: Tuple[int, str]
        for x in _make_loop().returning(True, True, False): pass
        for x in _make_loop().returning(True, True, outputs=False): pass
        for x in _make_loop().returning(True, inputs=True, outputs=False): pass
        for x in _make_loop().returning(enumerations=True, inputs=True, outputs=False): pass


def test_returning_before_map() -> None:
    def _calc_l_rate(word: str) -> float:
        return sum(char == 'l' for char in word) / len(word)

    def _make_loop() -> Loop[str, str, FALSE, FALSE, TRUE]:
        return loop_over(['hello', 'world'])

    def test_none() -> None:
        x: None
        for x in _make_loop().returning(outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(inputs=False, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, False, False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, False, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, inputs=False, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, inputs=False, outputs=False).map(_calc_l_rate): pass

    def test_outputs_only() -> None:
        x: float
        for x in _make_loop().returning().map(_calc_l_rate): pass
        for x in _make_loop().returning(outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(inputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(inputs=False, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, False, True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, False, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, inputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, inputs=False, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, inputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, inputs=False, outputs=True).map(_calc_l_rate): pass

    def test_inputs_outputs() -> None:
        x: Tuple[str, float]
        for x in _make_loop().returning(inputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(inputs=True, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, True, True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, True, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, inputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, inputs=True, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, inputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, inputs=True, outputs=True).map(_calc_l_rate): pass

    def test_inputs_only() -> None:
        x: str
        for x in _make_loop().returning(inputs=True, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, True, False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, True, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(False, inputs=True, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=False, inputs=True, outputs=False).map(_calc_l_rate): pass

    def test_enums_outputs() -> None:
        x: Tuple[int, float]
        for x in _make_loop().returning(True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, False).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, False, True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, False, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, inputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, inputs=False, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, inputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, inputs=False, outputs=True).map(_calc_l_rate): pass

    def test_enums_only() -> None:
        x: int
        for x in _make_loop().returning(True, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, False, False).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, False, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, inputs=False, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, inputs=False, outputs=False).map(_calc_l_rate): pass

    def test_enums_inputs_outputs() -> None:
        x: Tuple[int, str, float]
        for x in _make_loop().returning(True, True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, True, True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, True, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, inputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, inputs=True, outputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, inputs=True).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, inputs=True, outputs=True).map(_calc_l_rate): pass

    def test_enums_inputs() -> None:
        x: Tuple[int, str]
        for x in _make_loop().returning(True, True, False).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, True, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(True, inputs=True, outputs=False).map(_calc_l_rate): pass
        for x in _make_loop().returning(enumerations=True, inputs=True, outputs=False).map(_calc_l_rate): pass


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
