# %%
import inspect

from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC

InitScopeBasedIoCImplementationCmd().execute()


class Generate:
    @staticmethod
    def generate_dependency_injection(Class):
        # get signature of constructor
        constructor_signature = inspect.signature(Class.__init__)
        # get parameters from constructor
        constructor_parameters = constructor_signature.parameters
        # get argument's names
        argument_names = list(constructor_parameters.keys())
        # remove self from arguments
        if "self" in argument_names:
            argument_names.remove("self")
        # resolve arguments
        arguments = []
        for arg in argument_names:
            arguments.append(IoC.resolve(f"Parameters:{Class.__name__}.{arg}"))
        # generate and return strategy
        return lambda *args: Class(*arguments)


class PlayerName(str):
    pass


class Player:
    def __init__(self, age: int, weight: int, name: PlayerName):
        self.age = age
        self.weight = weight
        self.name = name


# %% 1. Проблема - приходится явно указывать тип зависимости и их количество
if __name__ == "__main__":
    IoC.resolve(
        "IoC.register",
        "dependency Player",
        lambda *args: Player(args[0], args[1], args[2]),
    ).execute()

    obj = IoC.resolve("dependency Player", 25, 88, PlayerName("Max"))
    print(obj.age, obj.weight, obj.name)

    IoC.resolve("IoC.unregister", "dependency Player").execute()

# %% 2. Регистрируем параметры заранее, а вот с количество так и осталась проблема
if __name__ == "__main__":
    IoC.resolve("IoC.register", "Players.age", lambda *args: 33).execute()
    IoC.resolve("IoC.register", "Players.weight", lambda *args: 100).execute()
    IoC.resolve("IoC.register", "Players.name", lambda *args: PlayerName("K")).execute()
    IoC.resolve(
        "IoC.register",
        "dependency Player",
        lambda *args: Player(
            IoC.resolve("Players.age"),
            IoC.resolve("Players.weight"),
            IoC.resolve("Players.name"),
        ),
    ).execute()

    obj = IoC.resolve("dependency Player")
    print(obj.age, obj.weight, obj.name)

    IoC.resolve("IoC.unregister", "dependency Player").execute()

# %% 3. Регистрация заранее осталась, а с количество боремся рефлексией
# конструктора класса
if __name__ == "__main__":
    IoC.resolve("IoC.register", "Parameters:Player.age", lambda *args: 25).execute()
    IoC.resolve("IoC.register", "Parameters:Player.weight", lambda *args: 96).execute()
    IoC.resolve(
        "IoC.register", "Parameters:Player.name", lambda *args: PlayerName("J")
    ).execute()
    IoC.resolve(
        "IoC.register",
        "dependency Player",
        Generate.generate_dependency_injection(Player),
    ).execute()
    obj = IoC.resolve("dependency Player")
    print(obj.age, obj.weight, obj.name)

    IoC.resolve("IoC.unregister", "dependency Player").execute()
