import inspect

from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC

InitScopeBasedIoCImplementationCmd().execute()


class Generator:
    @staticmethod
    def generate_dep_inj(Class):
        # Получить сигнатуру конструктора
        constructor_signature = inspect.signature(Class.__init__)
        # Извлечь параметры конструктора
        constructor_parameters = constructor_signature.parameters
        # Получить имена аргументов
        argument_names = list(constructor_parameters.keys())
        # Вывести имена аргументов
        print("Имена аргументов конструктора:", argument_names)

        for argument_name in argument_names:
            IoC.resolve(
                "IoC.register",
                argument_name,
                lambda *args: argument_name,
            ).execute()

        IoC.resolve(
            "IoC.register",
            f"{Class.__name__}",
            lambda *args: Class(*[IoC.resolve(arg) for arg in argument_names]),
        ).execute()


class Player:
    def __init__(self, age: int, weight: str, name: str):
        self.age = age
        self.weight = weight
        self.name = name


if __name__ == "__main__":
    IoC.resolve(
        "IoC.register",
        "Player",
        lambda *args: Player(args[0], args[1], args[2]),
        # lambda *args: Player(args[0], args[1], args[2], ....),
    ).execute()
    IoC.resolve(Player)


if __name__ == "__main__":
    IoC.resolve("IoC.register", "age", lambda *args: 25).execute()
    IoC.resolve("IoC.register", "weight", lambda *args: "96").execute()
    IoC.resolve("IoC.register", "name", lambda *args: "PlayerName").execute()

    IoC.resolve(
        "IoC.register",
        "Player",
        lambda *args: Player(
            IoC.resolve("age"),
            IoC.resolve("weight"),
            IoC.resolve("name"),
        ),
    ).execute()

    p = IoC.resolve("Player")
