# %%
import abc
import inspect

from spacegame.hw05.hw05 import UObject
from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC

InitScopeBasedIoCImplementationCmd().execute()
IoC.resolve(
    "IoC.register",
    "Spaceship.Operations.IMovable:position.get",
    lambda *args: args[0].get_property("position"),
).execute()
IoC.resolve(
    "IoC.register",
    "Spaceship.Operations.IMovable:velocity.get",
    lambda *args: args[0].get_property("velocity"),
).execute()
IoC.resolve(
    "IoC.register",
    "Spaceship.Operations.IMovable:position.set",
    lambda *args: args[0].set_property("position", args[1]),
).execute()  # тут могло быть что-то сложное (вплоть до нейронок)
IoC.resolve(
    "IoC.register",
    "Spaceship.Operations.IMovable:finish",
    lambda *args: print(f"hello from finish, {args}"),
).execute()


# %% -------------------------------------------------------------
class IMovable(abc.ABC):
    @abc.abstractmethod
    def get_position(self):
        pass

    @abc.abstractmethod
    def set_position(self, value):
        pass

    @abc.abstractmethod
    def get_velocity(self):
        pass

    @abc.abstractmethod
    def finish(self):
        pass


class TargetMovableAdapter(IMovable):
    def __init__(self, o: UObject):
        self.o = o

    def get_position(self):
        return IoC.resolve(
            "Spaceship.Operations.IMovable:position.get",
            self.o,
        )

    def get_velocity(self):
        return IoC.resolve(
            "Spaceship.Operations.IMovable:velocity.get",
            self.o,
        )

    def set_position(self, value):
        return IoC.resolve(
            "Spaceship.Operations.IMovable:position.set",
            self.o,
            value,
        )

    def finish(self):
        return IoC.resolve(
            "Spaceship.Operations.IMovable:finish",
            "fffinish",
        )


if __name__ == "__main__":
    obj = UObject()
    obj.set_property("position", [123, 123])
    obj.set_property("velocity", [321, 321])

    movable_obj = TargetMovableAdapter(obj)
    print(movable_obj.get_position())
    movable_obj.set_position([111, 111])
    print(movable_obj.get_position())
    print(movable_obj.get_velocity())

    movable_obj.finish()


# %% -------------------------------------------------------------
class IGenerator(abc.ABC):
    @abc.abstractstaticmethod
    def generate(dependency_space: str, IClass: object):
        pass


def generate(dependency_space: str, IClass: object):
    class_name = IClass.__name__
    class_attrs_names = [m[0] for m in inspect.getmembers(IClass, inspect.isfunction)]
    class_attrs = {}
    class_attrs["__init__"] = lambda slf, o: setattr(slf, "o", o)
    for attr_name in class_attrs_names:
        if attr_name[:4] == "get_":
            class_attrs[attr_name] = lambda slf: IoC.resolve(
                f"{dependency_space}.{class_name}:{attr_name[4:]}.get",
                slf.o,
            )
        elif attr_name[:4] == "set_":
            class_attrs[attr_name] = lambda slf, value: IoC.resolve(
                f"{dependency_space}.{class_name}:{attr_name[4:]}.set",
                slf.o,
                value,
            )
        else:
            class_attrs[attr_name] = lambda *args: IoC.resolve(
                f"{dependency_space}.{class_name}:{attr_name}",
                *args,
            )

    if class_name[:9] == "Interface" and class_name[9].isupper():
        adapter_class_name = class_name[9:]
    elif class_name[:1] == "I" and class_name[1].isupper():
        adapter_class_name = class_name[1:]
    else:
        adapter_class_name = class_name
    Adapter = type(
        f"{adapter_class_name}Adapter",
        (IClass,),
        class_attrs,
    )
    return Adapter


if __name__ == "__main__":
    obj = UObject()
    obj.set_property("position", [123, 123])
    obj.set_property("velocity", [321, 321])

    MovableAdapter = generate("Spaceship.Operations", IMovable)

    movable_obj = MovableAdapter(obj)
    print(movable_obj.get_position())
    movable_obj.set_position([111, 111])
    print(movable_obj.get_position())
    print(movable_obj.get_velocity())

    movable_obj.finish()

    print([m[0] for m in inspect.getmembers(MovableAdapter, inspect.isfunction)])

# %%
if __name__ == "__main__":
    IoC.resolve(
        "IoC.register",
        "Generator",
        lambda *args: generate(args[0], args[1]),
    ).execute()
    IoC.resolve(
        "IoC.register",
        "MovableAdapter",
        lambda *args: IoC.resolve("Generator", args[0], args[1]),
    ).execute()
    IoC.resolve(
        "IoC.register",
        "movable_object",
        lambda *args: IoC.resolve("MovableAdapter", args[0], args[1])(args[2]),
    ).execute()

    mov_obj = IoC.resolve(
        "movable_object",
        "Spaceship.Operations",
        IMovable,
        obj,
    )
    mov_obj.finish()
