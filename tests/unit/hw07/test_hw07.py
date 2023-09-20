# %%
from pathlib import Path
from queue import Queue

import pytest
from spacegame.hw05.hw05 import (
    MovableAdapter,
    MoveCmd,
    UObject,
    Vector,
)
from spacegame.hw07.hw07 import (
    BaseAppException,
    DoubleRepeateCmd,
    ExceptionHandler,
    LogPrintCmd,
    LogWriteCmd,
    RepeateCmd,
    SpecialErrorRaiserCmd,
)


def test_LogWriteCmd(mocker):
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_position",
        return_value=Vector([12, 5]),
    )
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_velocity",
        return_value=Vector([-7, 3]),
    )
    movable_obj = MovableAdapter(UObject())
    cmd = MoveCmd(movable_obj)
    exc = TypeError

    LogWriteCmd(cmd, exc).execute()

    fname = Path("log.txt")
    assert fname.exists()
    fname.unlink()


def test_RepeateCmd(mocker):
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_position",
        return_value=Vector([12, 5]),
    )
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_velocity",
        return_value=Vector([-7, 3]),
    )
    movable_obj = MovableAdapter(UObject())
    cmd = MoveCmd(movable_obj)

    RepeateCmd(cmd).execute()

    new_position = movable_obj.get_position()
    expected_position = Vector([5, 8])
    assert new_position == expected_position


def test_DoubleRepeateCmd(mocker):
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_position",
        return_value=Vector([12, 5]),
    )
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_velocity",
        return_value=Vector([-7, 3]),
    )
    movable_obj = MovableAdapter(UObject())
    cmd = MoveCmd(movable_obj)

    DoubleRepeateCmd(cmd).execute()

    new_position = movable_obj.get_position()
    expected_position = Vector([5, 8])
    assert new_position == expected_position


def test_SpecialErrorRaiserCmd():
    cmd = SpecialErrorRaiserCmd(TypeError)
    with pytest.raises(TypeError):
        cmd.execute()


def test_ExceptionHandler(mocker):
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_position",
        return_value=Vector([12, 5]),
    )
    mocker.patch(
        "spacegame.hw05.hw05.MovableAdapter.get_velocity",
        return_value=Vector([-7, 3]),
    )
    spaceship = UObject()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))

    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogWriteCmd(cmd, exc)),
    )

    while not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)

    fname = Path("log.txt")
    assert fname.exists()
    fname.unlink()
