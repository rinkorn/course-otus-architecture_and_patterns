# %%
import queue
import uuid

from spacegame.hw05.hw05 import ICommand
from spacegame.hw09.hw09 import (
    Dictionary,
    InitScopeBasedIoCImplementationCmd,
    IoC,
    IScope,
)
from spacegame.hw14.hw14 import NonBlockingCollection


class GameCmd(ICommand):
    """Очередь игры не обязательно потокобезопасная, т.к.
    игра уже лежит в потокобезопасной очереди
    """

    def __init__(self, game_name: str, parent_scope: IScope, init_game_cmd_names: list):
        self._game_name = game_name
        # receiver = IoC.resolve("IReceiver")
        self._queue = NonBlockingCollection()

        self._game_scope = IoC.resolve("scopes.new", parent_scope)
        IoC.resolve("scopes.current.set", self._game_scope).execute()

        print(id(parent_scope), parent_scope)
        print(id(self._game_scope), self._game_scope)
        print(id(IoC.resolve("scopes.current")), IoC.resolve("scopes.current"))

        IoC.resolve(
            "IoC.register",
            self._game_name + ".queue",
            lambda *args: self._queue,
        ).execute()
        IoC.resolve(
            "IoC.register",
            self._game_name + ".queue.put",
            lambda *args: self._queue.put(args[0]),
        ).execute()
        IoC.resolve(
            "IoC.register",
            self._game_name + ".queue.get",
            lambda *args: self._queue.get(),
        ).execute()

        game_objects = Dictionary()
        IoC.resolve(
            "IoC.register",
            "game_objects",
            lambda *args: game_objects,
        ).execute()
        players: int = IoC.resolve("Players")
        spaceships: int = IoC.resolve("Spaceships")
        for i_p in range(players):
            for i_s in range(spaceships):
                spaceship = IoC.resolve("Spaceship")
                for name in init_game_cmd_names:
                    IoC.resolve(name, spaceship).execute()
                # IoC.resolve(
                #     "Spaceship.label_and_add", spaceship, game_objects
                # ).execute()
                # IoC.resolve("Spaceship.assign_to", spaceship, player).execute()
                # IoC.resolve("Spaceship.locate", spaceship).execute()

    def execute(self):
        IoC.resolve("scopes.current.set", self._game_scope).execute()
        cmd = IoC.resolve(self._game_name + ".queue.get").execute()
        cmd.execute()


if __name__ == "__main__":
    InitScopeBasedIoCImplementationCmd().execute()
    IoC.resolve(
        "IoC.register",
        "Players",
        lambda *args: 2,
    ).execute()
    IoC.resolve(
        "IoC.register",
        "Spaceships",
        lambda *args: 3,
    ).execute()

    GameCmd(
        "game_id321",
        IoC.resolve("scopes.root"),
        ["label_and_add", "locate"],
    ).execute()
