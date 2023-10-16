# %%
from spacegame.hw05.hw05 import IMovable, MoveCmd, UObject, Vector
from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC
from spacegame.hw12.hw12 import Adapter, MoveCmdPluginCmd, RotateCmdPluginCmd


# %%
def get_initialized_movable_uobject():
    obj = UObject()
    obj.set_property("position", Vector([12.0, 5.0]))
    obj.set_property("velocity", Vector([-7.0, 3.0]))
    return obj


# %% initialization
def reinitialization():
    InitScopeBasedIoCImplementationCmd().execute()
    IoC.resolve(
        "scopes.current.set",
        IoC.resolve(
            "scopes.new",
            IoC.resolve("scopes.root"),
        ),
    ).execute()
    MoveCmdPluginCmd().execute()
    RotateCmdPluginCmd().execute()
    IoC.resolve(
        "IoC.register",
        "Adapter",
        lambda *args: Adapter.generate(args[0])(args[1]),
    ).execute()


# %% run code
if __name__ == "__main__":
    reinitialization()
    try:
        IoC.resolve("IoC.unregister", "Commands.Move").execute()
    except Exception as e:
        pass

    IoC.resolve(
        "IoC.register",
        "Commands.Move",
        lambda *args: MoveCmd(
            IoC.resolve("Adapter", args[0], args[1]),
        ).execute(),
    ).execute()

    obj = get_initialized_movable_uobject()
    IoC.resolve("Commands.Move", IMovable, obj)
    print(obj.get_property("position"))
    IoC.resolve("IoC.unregister", "Commands.Move").execute()


# %% это тоже самое что и выше
class CommandsStrategyBuilder:
    # main task for Builder
    # IoC.resolve("Commands.Move", obj)
    @staticmethod
    def build(ClassCmd):
        # TODO: need parse ClassCmd __init__, get uobject type and
        # replace args[0]
        return lambda *args: ClassCmd(
            IoC.resolve(
                "Adapter",
                args[0],  # IMovable (as example)
                args[1],
            )
        ).execute()


if __name__ == "__main__":
    reinitialization()

    obj = get_initialized_movable_uobject()
    try:
        IoC.resolve("IoC.unregister", "Commands.Move2").execute()
    except Exception as e:
        pass

    IoC.resolve(
        "IoC.register",
        "Commands.Move2",
        lambda *args: CommandsStrategyBuilder.build(MoveCmd)(*args),
    ).execute()
    IoC.resolve("Commands.Move2", IMovable, obj)
    print(obj.get_property("position"))
    IoC.resolve("IoC.unregister", "Commands.Move2").execute()

# %%
