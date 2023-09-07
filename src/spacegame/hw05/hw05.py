# %%
import abc
import math
from typing import Any


class IVector(abc.ABC):
    pass


class Vector(IVector):
    def __init__(self, data: list):
        if not isinstance(data, type(self) | list):
            raise TypeError("Wrong type of vector data.")
        if len(data) != 2:
            raise ValueError("Data length must be 2.")
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        if i > len(self):
            raise ValueError("Can't do that.")
        return self.data[i]

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Wrong type for add operation")
        self.data = [i + j for i, j in zip(self.data, other.data)]
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __eq__(self, other: object) -> bool:
        return self.data == other.data

    def __call__(self):
        return self.data

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return self.__str__()


def isVectorType(value):
    if isinstance(value, Vector):
        return True
    else:
        raise TypeError("Wrong type. Must be 'Vector'.")


class IUObject(abc.ABC):
    @abc.abstractmethod
    def get_property(self, attr: str):
        pass

    @abc.abstractmethod
    def set_property(self, attr: str, value: Any):
        pass


class UObject(IUObject):
    def __init__(self):
        self.hashmap = {}

    def get_property(self, attr: str):
        return self.hashmap[attr]

    def set_property(self, attr: str, value: Any):
        self.hashmap[attr] = value


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


class MoveAdapter(IMovable):
    def __init__(self, o: IUObject):
        self.o = o

    def get_position(self):
        return self.o.get_property("position")

    def get_velocity(self):
        d = self.o.get_property("direction")
        n = self.o.get_property("direction_numbers")
        v = self.o.get_property("velocity")
        # v0 = v[0] * math.cos(float(d) / 360 * n)
        # v1 = v[1] * math.sin(float(d) / 360 * n)
        v0 = v[0] * math.cos(float(d) / (2.0 * math.pi) * n)
        v1 = v[1] * math.sin(float(d) / (2.0 * math.pi) * n)
        print(math.cos(float(d) / (2.0 * math.pi) * n))
        print(math.sin(float(d) / (2.0 * math.pi) * n))
        print(math.cos(float(d) / 360 * n))
        print(math.sin(float(d) / 360 * n))
        print(v0, v1)
        return Vector([v0, v1])

    def set_position(self, new_position):
        self.o.set_property("position", new_position)


class MoveCmd(ICommand):
    def __init__(self, m: IMovable):
        self.m = m

    def execute(self):
        position = self.m.get_position()
        velocity = self.m.get_velocity()
        new_position = position + velocity
        self.m.set_position(new_position)


class IRotable(abc.ABC):
    @abc.abstractmethod
    def get_direction(self):
        pass

    @abc.abstractmethod
    def set_direction(self):
        pass


class RotateAdapter(IRotable):
    def __init__(self, o: IUObject):
        self.o = o

    def get_direction(self):
        return self.o.get_property("direction")

    def set_direction(self, new_direction: IVector):
        self.o.set_property("direction", new_direction)


class RotateCmd(ICommand):
    def __init__(self, r: IRotable):
        self.r = r

    def execute(self):
        d = self.r.get_direction()
        n = self.r.direction_number()
        v = self.r.angular_velocity()
        new_direction = d + v % n
        self.set_direction(new_direction)


if __name__ == "__main__":
    starship = UObject()
    starship.set_property("position", Vector([12.0, 5.0]))
    starship.set_property("velocity", Vector([-7.0, 3.0]))
    starship.set_property("direction", 0)
    starship.set_property("direction_numbers", 8)
    starship.set_property("angular_velocity", 0)

    MoveCmd(MoveAdapter(starship)).execute()

    print(starship.get_property("position"))
    # print(starship.get_property("direction"))

    # move = MoveCmd(p, v)
    # move.execute()
    # print(move.get_position())
    # m = MovableAdapter(p, v, d, av, dn)
    # print(m.get_position())
    # print(m.get_velocity())
    # m.set_position([1, 1])
