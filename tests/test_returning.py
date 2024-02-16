from src.loop import loop_over

from .utilities import assert_loops_as_expected


inp = list(range(0, 100, 2))
out = [x ** 2 for x in inp]
enums = list(range(len(inp)))
nones = len(inp) * [None]


def test_default():
    loop = loop_over(inp).map(pow, 2)
    assert_loops_as_expected(loop, out)


def test_none():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=False, inputs=False, outputs=False)
    assert_loops_as_expected(loop, nones)


def test_outputs_only():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=False, inputs=False, outputs=True)
    assert_loops_as_expected(loop, out)


def test_inputs_only():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=False, inputs=True, outputs=False)
    assert_loops_as_expected(loop, inp)


def test_inputs_and_outputs():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=False, inputs=True, outputs=True)
    assert_loops_as_expected(loop, zip(inp, out))


def test_enums_only():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=True, inputs=False, outputs=False)
    assert_loops_as_expected(loop, enums)


def test_enums_and_outputs():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=True, inputs=False, outputs=True)
    assert_loops_as_expected(loop, zip(enums, out))


def test_enums_and_inputs():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=True, inputs=True, outputs=False)
    assert_loops_as_expected(loop, zip(enums, inp))


def test_enums_inputs_and_outputs():
    loop = loop_over(inp).map(pow, 2).returning(enumerations=True, inputs=True, outputs=True)
    assert_loops_as_expected(loop, zip(enums, inp, out))
