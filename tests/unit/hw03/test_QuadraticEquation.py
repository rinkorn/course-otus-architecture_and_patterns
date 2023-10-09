import pytest
from spacegame.hw03.QuadraticEquation import (
    EPS,
    ConvertToFloatError,
    ParameterAZeroError,
    QuadraticEquation,
)


def test_QuadraticEquation_0():
    a, b, c = 1.0, 0.0, 1.0
    len_roots_expected = 0
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert len(roots) == len_roots_expected


def test_QuadraticEquation_1():
    a, b, c = 1.0, 0.0, -1.0
    roots_expected = [-1.0, 1.0]
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert (roots[0] - roots_expected[0]) < EPS
    assert (roots[1] - roots_expected[1]) < EPS


def test_QuadraticEquation_2():
    a, b, c = 1.0, 2.0, 1.0
    roots_expected = [-1.0]
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert (roots[0] - roots_expected[0]) < EPS


def test_QuadraticEquation_3():
    a, b, c = 0.0, 2.0, 1.0
    qe = QuadraticEquation(a, b, c)
    with pytest.raises(ParameterAZeroError):
        qe.solve()


def test_QuadraticEquation_4():
    a, b, c = 1.0, 2.0, 1.00000001
    roots_expected = [-1.0]
    qe = QuadraticEquation(a, b, c)
    roots = qe.solve()
    assert (roots[0] - roots_expected[0]) < EPS


@pytest.mark.parametrize(
    "a, b, c",
    [
        ("a", 2.0, 1.0),
        (1.0, "b", 1.0),
        (1.0, 2.0, "c"),
        ([1.0], 2.0, 1.0),
        (1.0, [2.0], 1.0),
        (1.0, 2.0, [1.0]),
        ("a", "b", ["c"]),
    ],
)
def test_QuadraticEquation_5(a, b, c):
    qe = QuadraticEquation(a, b, c)
    with pytest.raises(ConvertToFloatError):
        qe.solve()
