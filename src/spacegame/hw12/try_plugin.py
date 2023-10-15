from spacegame.hw05.hw05 import ICommand, IMovable
from spacegame.hw09.hw09 import IoC
from spacegame.hw12.hw12 import CommandsStrategyBuilder


def plugin(cls):
    # Внутри декоратора можно выполнять какие-либо действия с классом
    # или создавать новые атрибуты или методы для него.
    class ModifiedClass(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.extra_attribute = 42

    return ModifiedClass


@plugin
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
            lambda *args: args[0].set_property("position", args[1]),
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
