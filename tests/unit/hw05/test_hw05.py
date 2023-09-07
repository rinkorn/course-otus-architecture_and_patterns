import pytest
from spacegame.hw05.hw05 import (
    IMovable,
    IRotable,
    Move,
    MoveAdapter,
    Rotate,
    UObject,
    Vector,
)


def test_Move_0():
    position = Vector([12, 5])
    velocity = Vector([-7, 3])
    m = Move(position, velocity)
    m.execute()
    new_postition = m.get_position()
    expected_position = Vector([5, 8])
    assert m.get_position() == expected_position


def test_Move_1():
    position = None
    velocity = Vector([-7, 3])
    # velocity = mocker.patch('Vector', return_value=[-7, 3])
    with pytest.raises(Exception):
        m = Move(position, velocity)
        m.execute()


def test_Move_2(mocker):
    position = Vector([12, 5])
    velocity = None
    with pytest.raises(Exception):
        m = Move(position, velocity)
        m.execute()


def test_Move_3():
    position = Vector([12, 5])
    velocity = Vector([-7, 3])
    m = Move(position, velocity)
    # m.execute()
    with pytest.raises(Exception):
        m.set_position([25, -1])
        # m.set_position(Vector([25, -1]))


# def test_Move_1(mocker):
#     position = Vector([0, 0])
#     velocity = Vector([0, 0])
#     m = Move(position, velocity)
#     mock_position = mocker.patch("hw05.Move.position")
#     mock_velocity = mocker.patch("hw05.Move.velocity")
#     mock_position.return_value = Vector([12, 5])
#     mock_velocity.return_value = Vector([-7, 3])
#     # print(m.position)
#     # print(m.velocity)
#     m.execute()
#     new_position = m.get_position()
#     expected_position = Vector([5, 8])
#     assert new_position == expected_position
