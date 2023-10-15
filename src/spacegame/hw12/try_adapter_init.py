import abc

from spacegame.hw05.hw05 import ICommand, UObject
from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC
from spacegame.hw12.hw12 import CommandsStrategyBuilder

# HOW TO USE GetPropertyCmd????
# class GetPropertyCmd(ICommand):
#     def __init__(self, o: UObject, key: str):
#         self.o = o
#         self.key = key

#     def execute(self):
#         self.o.get_property(self.key)


class SetPropertyCmd(ICommand):
    def __init__(self, o: UObject, key: str, value: any):
        self.o = o
        self.key = key
        self.value = value

    def execute(self):
        self.o.set_property(self.key, self.value)


class MoveCmdPluginCmd(ICommand):
    def execute(self):
        IoC.resolve(
            "IoC.register",
            f"{IMovable.__module__}.IMovable:position.get",
            lambda *args: args[0].get_property("position"),
        ).execute()
        IoC.resolve(
            "IoC.register",
            f"{IMovable.__module__}.IMovable:velocity.get",
            lambda *args: args[0].get_property("velocity"),
        ).execute()
        IoC.resolve(
            "IoC.register",
            f"{IMovable.__module__}.IMovable:position.set",
            lambda *args: SetPropertyCmd(args[0], "position", args[1]).execute(),
            # lambda *args: args[0].set_property("position", args[1]),
        ).execute()  # тут могло быть что-то сложное (вплоть до нейронок)
        IoC.resolve(
            "IoC.register",
            f"{IMovable.__module__}.IMovable:finish",
            lambda *args: print(f"hello from finish, {args}"),
        ).execute()
        IoC.resolve(
            "IoC.register",
            f"{IMovable.__module__}.Commands:Move",
            lambda *args: CommandsStrategyBuilder.build(IMovable),
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
    """Need generate this Movable adapter"""

    def __init__(self, o: UObject):
        self.o = o

    def get_position(self):
        return IoC.resolve(
            f"{IMovable.__module__}.IMovable:position.get",
            self.o,
        )

    def get_velocity(self):
        return IoC.resolve(
            f"{IMovable.__module__}.IMovable:velocity.get",
            self.o,
        )

    def set_position(self, value):
        return IoC.resolve(
            f"{IMovable.__module__}.IMovable:position.set",
            self.o,
            value,
        )

    def finish(self):
        return IoC.resolve(
            f"{IMovable.__module__}.IMovable:finish",
            "fffinish",
        )


if __name__ == "__main__":
    InitScopeBasedIoCImplementationCmd().execute()
    MoveCmdPluginCmd().execute()
    obj = UObject()
    obj.set_property("position", [123, 123])
    obj.set_property("velocity", [321, 321])

    movable_obj = TargetMovableAdapter(obj)
    print(movable_obj.get_position())
    print(movable_obj.get_velocity())
    movable_obj.set_position([111, 111])
    print(movable_obj.get_position())
    print(movable_obj.get_velocity())

    movable_obj.finish()
