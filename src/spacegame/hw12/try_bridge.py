import abc

from spacegame.hw05.hw05 import ICommand, MoveCmd, RotateCmd
from spacegame.hw07.hw07 import DoNothingCmd, RepeateCmd
from spacegame.hw08.hw08 import (
    BurnFuelVolumeCmd,
    CheckFuelVolumeCmd,
    MacroCmd,
)


class IInjectable(abc.ABC):
    @abc.abstractmethod
    def inject(self, cmd: ICommand):
        pass


class BridgeCmd(ICommand, IInjectable):
    def inject(self, cmd: ICommand):
        self.cmd = cmd

    def execute(self):
        self.cmd.execute()


if __name__ == "__main__":
    move = MoveCmd()
    rotate = RotateCmd()
    check_fuel = CheckFuelVolumeCmd()
    burn_fuel = BurnFuelVolumeCmd()
    bridge = BridgeCmd()

    cmds = (move, rotate, check_fuel, burn_fuel)
    going_cmd_impl = MacroCmd(*cmds)
    # going_cmd_impl = IoC.resolve("Movement", *cmds)

    # сделать повторяющуюся команду
    bridge.inject(MacroCmd(going_cmd_impl, RepeateCmd(bridge)))

    # если нужно отменить команду
    bridge.inject(DoNothingCmd())
