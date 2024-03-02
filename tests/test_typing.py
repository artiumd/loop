from typing import List, Dict, Tuple
from itertools import product

from src.loop import loop_range, loop_over, Loop


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


def test_returning() -> None:
    def _make_loop() -> Loop[str, float, float]:
        return loop_over(['hello', 'world']).map(lambda word: sum(char == 'l' for char in word) / len(word))
    
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


def _print_raw_options():
    options = ['missing', 'pos_false', 'pos_true', 'named_false', 'named_true']
    for x in product(options, options, options):
        # pos cant come after missing or named
        if (x[1].startswith('pos') and (x[0] == 'missing' or x[0].startswith('named'))) or \
           (x[2].startswith('pos') and ('missing' in x[:2] or x[0].startswith('named') or x[1].startswith('named'))):
            continue

        print(x)
