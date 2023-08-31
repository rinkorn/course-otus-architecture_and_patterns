import pytest
from spacegame.hw03.QuadraticEquation import (
    ConvertToFloatError,
    ParameterAZeroError,
    QuadraticEquation,
)


def test_QuadraticEquation_0():
    a, b, c = 1, 0, 1
    roots_expected = []
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert roots == roots_expected


def test_QuadraticEquation_1():
    a, b, c = 1, 0, -1
    roots_expected = [-1, 1]
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert roots == roots_expected


def test_QuadraticEquation_2():
    a, b, c = 1, 2, 1
    roots_expected = [-1]
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert roots == roots_expected


def test_QuadraticEquation_3():
    a, b, c = 0, 2, 1
    roots_expected = []  # noqa
    qe = QuadraticEquation(a, b, c)
    with pytest.raises(ParameterAZeroError):
        qe.solve()


def test_QuadraticEquation_4():
    a, b, c = 1, 2, 1.00000001
    roots_expected = [-1]
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert roots == roots_expected


@pytest.mark.parametrize(
    "a, b, c",
    [
        ("a", 2, 1),
        (1, "b", 1),
        (1, 2, "c"),
        ([1], 2, 1),
        (1, [2], 1),
        (1, 2, [1]),
        ("a", "b", ["c"]),
    ],
)
def test_QuadraticEquation_5(a, b, c):
    qe = QuadraticEquation(a, b, c)
    with pytest.raises(ConvertToFloatError):
        qe.solve()
