# %%
import abc
import math


class Vector:
    def __init__(self, data=[]):
        if not isinstance(data, type(self) | list):
            raise TypeError("Wrong type of vector data.")
        if len(data) != 2:
            raise ValueError("Data length must be 2.")
        self.data = data

    def __len__(self):
        return len(self.data)

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


class Movable(abc.ABC):
    @abc.abstractmethod
    def get_position(self):
        pass

    @abc.abstractmethod
    def get_velocity(self):
        pass

    @abc.abstractmethod
    def set_position(self):
        pass


class Move(Movable):
    def __init__(self, position: Vector, velocity: Vector):
        if isVectorType(position):
            self.position = position
        if isVectorType(velocity):
            self.velocity = velocity

    def get_position(self):
        try:
            return self.position
        except:  # noqa
            raise ValueError("Can't get position")

    def get_velocity(self):
        try:
            return self.velocity
        except:  # noqa
            raise ValueError("Can't get velocity")

    def set_position(self, new_position):
        if isVectorType(new_position):
            self.position = new_position

    def execute(self):
        position = self.get_position()
        velocity = self.get_velocity()
        new_position = position + velocity
        self.set_position(new_position)


class Rotable(abc.ABC):
    @abc.abstractmethod
    def get_direction(self):
        pass

    @abc.abstractmethod
    def set_direction(self):
        pass


class Rotate(Rotable):
    def __init__(self, direction, angular_velocity, direction_numbers):
        self.direction = direction
        self.angular_velocity = angular_velocity
        self.direction_numbers = direction_numbers

    def get_direction(self):
        return self.direction

    def set_direction(self, new_direction):
        self.direction = new_direction

    def execute(self):
        d = self.get_direction()
        v = self.angular_velocity()
        new_direction = d + v % self.direction_numbers
        self.set_direction(new_direction)


class IUObject(abc.ABC):
    @abc.abstractmethod
    def get_property(self, attr):
        pass

    @abc.abstractmethod
    def set_property(self, attr, value):
        pass


class UObject(IUObject):
    def get_property(self, attr):
        return self.__dict__[attr]

    def set_property(self, attr, value):
        self.__dict__[attr] = value


class MovableAdapter(Movable, Rotable, UObject):
    def __init__(
        self, position, velocity, direction, angular_velocity, direction_numbers
    ):
        self.position = position
        self.velocity = velocity
        self.direction = direction
        self.angular_velocity = angular_velocity
        self.direction_numbers = direction_numbers

    def get_property(self, attr):
        # return super().get_property(attr)
        return self.__dict__[attr]

    def set_property(self, attr, value):
        # return super().set_property(attr, value)
        self.__dict__[attr] = value

    def get_position(self):
        return self.get_property("position")

    def set_position(self, new_position):
        self.set_property("position", new_position)

    def get_velocity(self):
        d = self.get_property("direction")
        dn = self.get_property("direction_numbers")
        v = self.get_property("velocity")

        d = float(d)
        v0 = v[0] * math.cos(d / (2 * math.pi) * dn)
        v1 = v[1] * math.sin(d / (2 * math.pi) * dn)
        new_v = [v0, v1]
        return new_v

    def get_direction(self):
        return super().get_direction()

    def set_direction(self):
        return super().set_direction()


if __name__ == "__main__":
    position = p = Vector([12, 5])
    velocity = v = Vector([-7, 3])
    direction = d = 0
    angular_velocity = av = 0
    direction_numbers = dn = 8
    move = Move(p, v)
    move.execute()
    print(move.get_position())
    # m = MovableAdapter(p, v, d, av, dn)
    # print(m.get_position())
    # print(m.get_velocity())
    # m.set_position([1, 1])
