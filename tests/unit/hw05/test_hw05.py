import os

import pytest
from spacegame.hw05.hw05 import (
    IMovable,
    IUObject,
    IVector,
    MovableAdapter,
    MoveCmd,
    UObject,
    Vector,
)

"""
Остался вопрос к тому что именно нужно мокать, UObject или MoveAdapter

Если честно, то до конца не понял как писать предложенные тесты.

Может быть есть правильные примеры на python?
"""


def test_Move_0(mocker):
    """
    Для объекта, находящегося в точке (12, 5) и движущегося со скоростью
    (-7, 3) движение меняет положение объекта на (5, 8)
    """
    mock = mocker.patch("spacegame.hw05.hw05.MoveAdapter.get_position")
    mock.return_value = Vector([12, 5])
    mock = mocker.patch("spacegame.hw05.hw05.MoveAdapter.get_velocity")
    mock.return_value = Vector([-7, 3])

    obj = UObject()
    movable_obj = MovableAdapter(obj)
    cmd = MoveCmd(movable_obj)
    cmd.execute()
    new_position = movable_obj.get_position()
    expected_position = Vector([5, 8])
    assert new_position == expected_position


def test_Move_1(mocker):
    """
    Попытка сдвинуть объект, у которого невозможно прочитать
    положение в пространстве, приводит к ошибке
    """
    mock = mocker.patch("spacegame.hw05.hw05.MoveAdapter.get_velocity")
    mock.return_value = Vector([-7, 3])

    obj = UObject()
    movable_obj = MovableAdapter(obj)
    cmd = MoveCmd(movable_obj)
    with pytest.raises(Exception):
        cmd.execute()


def test_Move_2(mocker):
    """
    Попытка сдвинуть объект, у которого невозможно прочитать
    значение мгновенной скорости, приводит к ошибке
    """
    mock = mocker.patch("spacegame.hw05.hw05.MoveAdapter.get_position")
    mock.return_value = Vector([12, 5])

    obj = UObject()
    movable_obj = MovableAdapter(obj)
    cmd = MoveCmd(movable_obj)
    with pytest.raises(Exception):
        cmd.execute()


def test_Move_3(mocker):
    """
    Попытка сдвинуть объект, у которого невозможно изменить
    положение в пространстве, приводит к ошибке
    """
    mock = mocker.patch("spacegame.hw05.hw05.MoveAdapter.get_position")
    mock.return_value = Vector([12, 5])
    mock = mocker.patch("spacegame.hw05.hw05.MoveAdapter.get_velocity")
    mock.return_value = Vector([-7, 3])
    mock = mocker.patch("spacegame.hw05.hw05.MoveAdapter.get_velocity")
    mock.return_value = ValueError

    obj = UObject()
    movable_obj = MovableAdapter(obj)
    cmd = MoveCmd(movable_obj)
    with pytest.raises(Exception):
        cmd.execute()
