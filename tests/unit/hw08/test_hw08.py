# %%
import pytest
from spacegame.hw05.hw05 import (
    UObject,
    Vector,
)
from spacegame.hw07.hw07 import (
    DoNothingCmd,
    SpecialErrorRaiserCmd,
)
from spacegame.hw08.hw08 import (
    BurnFuelVolumeCmd,
    ChangeVelocityCmd,
    CheckFuelVolumeCmd,
    CommandException,
    MacroCmd,
)


@pytest.mark.parametrize(
    "fuel_volume",
    [
        1234,
        1,
        0,
        pytest.param(-1, marks=pytest.mark.xfail(raises=CommandException)),
        pytest.param(-4321, marks=pytest.mark.xfail(raises=CommandException)),
    ],
)
def test_CheckFuelVolumeCmd(fuel_volume):
    # pre
    obj = UObject()
    obj.set_property("fuel_volume", fuel_volume)
    # action
    cmd = CheckFuelVolumeCmd(obj)
    cmd.execute()
    # post


@pytest.mark.parametrize(
    "fuel_volume,fuel_volume_expected",
    [
        (1234, 1233),
        (1, 0),
        (0, 0),
        (-1, 0),
        (-4321, 0),
    ],
)
def test_BurnFuelVolumeCmd(fuel_volume, fuel_volume_expected):
    # pre
    obj = UObject()
    obj.set_property("fuel_volume", fuel_volume)
    # action
    cmd = BurnFuelVolumeCmd(obj)
    cmd.execute()
    # post
    fuel_volume_new = obj.get_property("fuel_volume")
    assert fuel_volume_expected == fuel_volume_new


@pytest.mark.parametrize(
    "cmds",
    [
        [],
        [DoNothingCmd()],
        [DoNothingCmd(), DoNothingCmd()],
        pytest.param(
            [SpecialErrorRaiserCmd(ValueError)],
            marks=pytest.mark.xfail(raises=CommandException),
        ),
        pytest.param(
            [
                DoNothingCmd(),
                SpecialErrorRaiserCmd(ValueError),
                DoNothingCmd(),
            ],
            marks=pytest.mark.xfail(raises=CommandException),
        ),
    ],
)
def test_MacroCmd(cmds):
    # pre
    # action
    cmd = MacroCmd(*cmds)
    cmd.execute()
    # post


@pytest.mark.parametrize(
    "velocity,direction,direction_numbers,velocity_expected",
    [
        (Vector([0.0, 0.0]), 0, 8, Vector([0.0, 0.0])),
        (Vector([0.0, 0.0]), 5, 215, Vector([0.0, 0.0])),
        (Vector([0.0, 1.0]), 0, 8, Vector([0.0, 1.0])),
        (Vector([0.0, 1.0]), 1, 8, Vector([0.7071067, 0.7071067])),
        (Vector([0.0, 1.0]), 2, 8, Vector([1.0, 0.0])),
        (Vector([0.0, 1.0]), 3, 8, Vector([0.7071067, -0.7071067])),
        (Vector([0.0, 1.0]), 4, 8, Vector([0.0, -1.0])),
        (Vector([0.0, 1.0]), 5, 8, Vector([-0.7071067, -0.7071067])),
        (Vector([0.0, 1.0]), 6, 8, Vector([-1.0, 0.0])),
        (Vector([0.0, 1.0]), 7, 8, Vector([-0.7071067, 0.7071067])),
        (Vector([0.0, 1.0]), 8, 8, Vector([0.0, 1.0])),
        (Vector([0.0, 1.0]), 9, 8, Vector([0.7071067, 0.7071067])),
        (Vector([0.0, 1.0]), 1234, 8, Vector([1.0, 0.0])),
        (Vector([0.0, 1.0]), -1234, 8, Vector([-1.0, 0.0])),
        (Vector([0.0, 1.0]), 0, 360, Vector([0.0, 1.0])),
        (Vector([0.0, 1.0]), 1, 360, Vector([0.0174524, 0.999847695])),
        pytest.param(
            [0.0, 1.0],
            0,
            8,
            [0.0, 1.0],
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(
            Vector([0.0, 1.0]),
            0,
            8,
            [0.0, 1.0],
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ],
)
def test_ChangeVelocityCmd(velocity, direction, direction_numbers, velocity_expected):
    # pre
    obj = UObject()
    obj.set_property("velocity", velocity)
    obj.set_property("direction", direction)
    obj.set_property("direction_numbers", direction_numbers)
    # action
    cmd = ChangeVelocityCmd(obj)
    cmd.execute()
    # post
    velocity_new = obj.get_property("velocity")
    assert velocity_expected == velocity_new
