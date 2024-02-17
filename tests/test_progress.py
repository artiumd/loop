from typing import List
import re
import io

import pytest

from src.loop import loop_over, Loop


re.purge()


def test_no_progress(capsys):
    loop_over(range(10000)).exhaust()
    captured = capsys.readouterr()
    assert captured.err == '', captured.err


def test_bare():    
    n = 10
    iterable = (i for i in range(n))
    loop = loop_over(iterable)
    prints = _capture_tqdm_outputs_without_newlines(loop)

    # Positive
    pattern = rf'{n}it \[.+:.+, .+\]'
    assert re.fullmatch(pattern, prints[-1])

    # Negative
    with pytest.raises(AssertionError):
        pattern = rf'{n}it  \[.+:.+, .+\]'
        assert re.fullmatch(pattern, prints[-1])


def test_length():    
    n = 10
    loop = loop_over(range(n))
    prints = _capture_tqdm_outputs_without_newlines(loop, total=len)

    # Positive
    pattern = rf'100%\|(.*)\| {n}/{n} \[.+<.+, .+\]'
    assert re.fullmatch(pattern, prints[-1])

    # Negative
    with pytest.raises(AssertionError):
        pattern = rf'100%\|(.*)\|  {n}/{n} \[.+<.+, .+\]'
        assert re.fullmatch(pattern, prints[-1])


def test_desc():
    n = 10
    desc = 'some description'
    loop = loop_over(range(n))
    prints = _capture_tqdm_outputs_without_newlines(loop, desc=desc, total=len)
    
    # Positive
    pattern = rf'{desc}: 100%\|(.*)\| {n}/{n} \[.+<.+, .+\]'
    assert re.fullmatch(pattern, prints[-1])

    # Negative
    with pytest.raises(AssertionError):
        pattern = rf'100%\|(.*)\|  {n}/{n} \[.+<.+, .+\]'
        assert re.fullmatch(pattern, prints[-1])


def test_static_postifx():
    postfix = 'static postfix'
    n = 10
    loop = loop_over(range(n))
    prints = _capture_tqdm_outputs_without_newlines(loop, total=len, postfix_str=postfix)
    
    # Positive
    pattern = rf'100%\|(.*)\| {n}/{n} \[.+<.+, .+, {postfix}\]'
    assert re.fullmatch(pattern, prints[-1])

    # Negative
    with pytest.raises(AssertionError):
        pattern = rf'100%\|(.*)\| {n}/{n} \[.+<.+, .+\,\]'
        assert re.fullmatch(pattern, prints[-1])


def test_dynamic_postfix():
    inp = list(range(0, 100, 2))
    out = [x**2 for x in inp]
    loop = loop_over(inp).map(pow, 2).returning(enumerations=True, inputs=True, outputs=True)
    prints = _capture_tqdm_outputs_without_newlines(loop, total=len, postfix_str=lambda x: f'idx={x[0]},inp={x[1]},out={x[2]}')

    # Positive
    pattern = rf'100%\|(.*)\| {len(inp)}/{len(inp)} \[.+<.+, .+, idx={len(inp) - 1},inp={inp[-1]},out={out[-1]}\]'
    assert re.fullmatch(pattern, prints[-1])


def _capture_tqdm_outputs_without_newlines(loop: Loop, **kwargs) -> List[str]:
    with io.StringIO() as file:
        loop.show_progress(refresh=True, file=file, **kwargs).exhaust()
        output = file.getvalue()

    outputs = [part.rstrip() for part in output.split('\r')]

    return outputs
