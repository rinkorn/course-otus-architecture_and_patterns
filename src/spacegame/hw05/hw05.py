# %%
import abc
import math
from typing import Any


class IVector(abc.ABC):
    @abc.abstractmethod
    def __len__(self):
        pass

    @abc.abstractmethod
    def __getitem__(self, i):
        pass

    @abc.abstractmethod
    def __add__(self, other):
        pass

    @abc.abstractmethod
    def __radd__(self, other):
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __call__(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass


class Vector(IVector):
    def __init__(self, coords: list):
        if not isinstance(coords, type(self) | list):
            raise TypeError("Wrong type of vector data.")
        if len(coords) != 2:
            raise ValueError("Data length must be 2.")
        self.coords = coords

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        if i > len(self):
            raise ValueError("Can't do that.")
        return self.coords[i]

    def __add__(self, other: IVector):
        if not isinstance(other, type(self)):
            raise TypeError("Wrong type for add operation")
        self.coords = [i + j for i, j in zip(self.coords, other.coords)]
        return self

    def __radd__(self, other: IVector):
        return self.__add__(other)

    def __eq__(self, other: IVector) -> bool:
        return self.coords == other.coords

    def __call__(self):
        return self.coords

    def __str__(self) -> str:
        return str(self.coords)

    def __repr__(self) -> str:
        return self.__str__()


class IUObject(abc.ABC):
    @abc.abstractmethod
    def get_property(self, key: str):
        pass

    @abc.abstractmethod
    def set_property(self, key: str, value: Any):
        pass


class UObject(IUObject):
    def __init__(self):
        self.hashtable = {}

    def get_property(self, key: str):
        return self.hashtable[key]

    def set_property(self, key: str, value: Any):
        self.hashtable[key] = value


class ICommand(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass


class IMovable(abc.ABC):
    @abc.abstractmethod
    def get_position(self):
        pass

    @abc.abstractmethod
    def get_velocity(self):
        pass

    @abc.abstractmethod
    def set_position(self):
        pass


class MovableAdapter(IMovable):
    """
    Откуда MovableAdapter знает про "direction", "velocity" и др., не относящиеся
    к этому объекту напрямую по смыслу (move)?
    В дальнейшем можем отказаться от поворотов и нужно будет править код?
    """

    def __init__(self, o: IUObject):
        self.o = o

    def get_position(self):
        return self.o.get_property("position")

    def get_velocity(self):
        # d = self.o.get_property("direction")
        # dn = self.o.get_property("direction_numbers")
        # v = self.o.get_property("velocity")
        # new_velocity = Vector(
        #     [
        #         v[0] * math.cos(float(d) / 360 * dn),
        #         v[1] * math.sin(float(d) / 360 * dn),
        #     ]
        # )
        # return new_velocity
        return self.o.get_property("velocity")

    def set_position(self, position: IVector):
        self.o.set_property("position", position)


class MoveCmd(ICommand):
    def __init__(self, obj: IMovable):
        self.obj = obj

    def execute(self):
        position = self.obj.get_position()
        velocity = self.obj.get_velocity()
        new_position = position + velocity
        self.obj.set_position(new_position)


class IRotable(abc.ABC):
    @abc.abstractmethod
    def get_direction(self):
        pass

    @abc.abstractmethod
    def get_direction_numbers(self):
        pass

    @abc.abstractmethod
    def get_angular_velocity(self):
        pass

    @abc.abstractmethod
    def set_direction(self):
        pass


class RotableAdapter(IRotable):
    def __init__(self, o: IUObject):
        self.o = o

    def get_direction(self):
        return self.o.get_property("direction")

    def get_direction_numbers(self):
        return self.o.get_property("direction_numbers")

    def get_angular_velocity(self):
        return self.o.get_property("angular_velocity")

    def set_direction(self, direction: IVector):
        self.o.set_property("direction", direction)


class RotateCmd(ICommand):
    def __init__(self, obj: IRotable):
        self.obj = obj

    def execute(self):
        d = self.obj.get_direction()
        av = self.obj.get_angular_velocity()
        n = self.obj.get_direction_numbers()
        new_direction = (d + av) % n
        self.obj.set_direction(new_direction)


if __name__ == "__main__":
    starship = UObject()
    starship.set_property("position", Vector([12.0, 5.0]))
    starship.set_property("velocity", Vector([-7.0, 3.0]))
    starship.set_property("direction", 0)
    starship.set_property("direction_numbers", 8)
    starship.set_property("angular_velocity", -1)

    cmd = MoveCmd(MovableAdapter(starship))
    cmd.execute()
    print(starship.get_property("position"))

    cmd = RotateCmd(RotableAdapter(starship))
    cmd.execute()
    print(starship.get_property("direction"))
