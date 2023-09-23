import abc
import math

from spacegame.hw05.hw05 import (
    ICommand,
    IMovable,
    IRotable,
    IUObject,
    IVector,
    MovableAdapter,
    MoveCmd,
    RotableAdapter,
    RotateCmd,
    UObject,
    Vector,
)
from spacegame.hw07.hw07 import DoNothingCmd


# %%
class CommandException(Exception):
    pass


# %%
class IFuelable(abc.ABC):
    @abc.abstractmethod
    def get_fuel_volume(self):
        pass

    @abc.abstractmethod
    def set_fuel_volume(self):
        pass


class FuelableAdapter(IFuelable):
    def __init__(self, o: IUObject):
        self.o = o

    def get_fuel_volume(self):
        return self.o.get_property("fuel_volume")

    def set_fuel_volume(self, fuel_volume: int):
        self.o.set_property("fuel_volume", fuel_volume)


class CheckFuelVolumeCmd(ICommand):
    """Реализовать класс CheckFuelComamnd"""

    def __init__(self, o: IUObject):
        self.o = o

    def execute(self):
        fuel_volume = FuelableAdapter(self.o).get_fuel_volume()
        if fuel_volume <= 0:
            raise CommandException("Fuel is empty")


class BurnFuelVolumeCmd(ICommand):
    """Реализовать класс BurnFuelCommand"""

    def __init__(self, o: IUObject):
        self.o = o

    def execute(self):
        fuel_volume = FuelableAdapter(self.o).get_fuel_volume()
        fuel_volume = fuel_volume - 1
        fuel_volume = max(0, fuel_volume)
        FuelableAdapter(self.o).set_fuel_volume(fuel_volume)


class MacroCmd(ICommand):
    """
    Реализовать простейшую макрокоманду.
    Здесь простейшая - это значит, что при выбросе исключения
    вся последовательность команд приостанавливает свое выполнение,
    а макрокоманда выбрасывает CommandException.
    """

    def __init__(self, cmds: list):
        self.cmds = cmds

    def execute(self):
        try:
            for cmd in self.cmds:
                cmd.execute()
        except Exception:
            raise CommandException("Can't execute MacroCmd")


class MoveWithFuelBurnCmd(ICommand):
    """
    Реализовать команду движения по прямой с расходом топлива,
    используя команды с предыдущих шагов.
    """

    def __init__(self, o: IUObject):
        self.o = o

    def execute(self):
        cmds = []
        cmds.append(CheckFuelVolumeCmd(self.o))
        cmds.append(MoveCmd(MovableAdapter(self.o)))
        cmds.append(BurnFuelVolumeCmd(self.o))
        MacroCmd(cmds).execute()


# %%
class IChangableVelocity(abc.ABC):
    @abc.abstractmethod
    def get_velocity(self):
        pass

    @abc.abstractmethod
    def set_velocity(self):
        pass


class ChangableVelocityAdapter(IChangableVelocity):
    def __init__(self, o: IUObject):
        self.o = o

    def get_velocity(self):
        return self.o.get_property("velocity")

    def set_velocity(self, velocity: int):
        self.o.set_property("velocity", velocity)


class ChangeVelocityCmd(ICommand):
    """Реализовать команду для модификации вектора мгновенной скорости при повороте.
    Необходимо учесть, что не каждый разворачивающийся объект движется."""

    def __init__(self, o: IUObject):
        self.o = o

    def execute(self):
        velocity = ChangableVelocityAdapter(self.o).get_velocity()
        direction = RotableAdapter(self.o).get_direction()
        direction_numbers = RotableAdapter(self.o).get_direction_numbers()
        R = math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
        alpha = math.radians(float(direction) * 360 / direction_numbers)
        new_velocity = Vector(
            [
                R * math.cos(alpha),
                R * math.sin(alpha),
            ]
        )
        ChangableVelocityAdapter(self.o).set_velocity(new_velocity)


# %%
class RotateChangeVelocityCmd(ICommand):
    """
    Реализовать команду поворота, которая еще и меняет вектор мгновенной скорости,
    если есть.
    """

    def __init__(self, o: IUObject):
        self.o = o

    def execute(self):
        cmds = []
        cmds.append(RotateCmd(RotableAdapter(self.o)))
        cmds.append(ChangeVelocityCmd(self.o))
        MacroCmd(cmds).execute()


# %%
if __name__ == "__main__":
    spaceship = UObject()
    spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 1)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)
    spaceship.set_property("fuel_volume", 2)

    MoveWithFuelBurnCmd(spaceship).execute()
    for key, value in spaceship.store.items():
        print(key, value)
    print()

    ChangeVelocityCmd(spaceship).execute()
    for key, value in spaceship.store.items():
        print(key, value)
    print()

    RotateChangeVelocityCmd(spaceship).execute()
    for key, value in spaceship.store.items():
        print(key, value)
    print()
