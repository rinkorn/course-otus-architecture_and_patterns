import abc

from spacegame.hw05.hw05 import MovableAdapter, MoveCmd, UObject
from spacegame.hw08.hw08 import MacroCmd
from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC


class Generator:
    def get(self, key):
        pass


class OperationBuilder:
    def __init__(self, name: str):
        self.cmd_name = name

    def build(self, *args: any):
        uobject = args[0]
        cmds_name = IoC.resolve(self.cmd_name + ".Description")
        cmds = [IoC.resolve(name, uobject) for name in cmds_name]
        return MacroCmd(*cmds)


if __name__ == "__main__":
    InitScopeBasedIoCImplementationCmd().execute()
    uobject = UObject()

    # typeof = base

    IoC.resolve(
        "IoC.register",
        "command.Move",
        lambda *args: MoveCmd(MovableAdapter(args[0])),
    ).execute()

    # IoC.resolve(
    #     "IoC.register",
    #     "command.Move",
    #     Generator.get(typeof(MoveCmd)),
    # ).execute()]

    IoC.resolve("command.Move", uobject)
    # IoC.resolve("command.Rotate", uobject)
    # IoC.resolve("command.Fireable", uobject)

    # IoC.resolve(
    #     "IoC.register",
    #     "operations.Movement",
    #     lambda *args: OperationBuilder("operations.movement").build(),
    # ).execute()

    # IoC.resolve("operations.Movement", uobject)
