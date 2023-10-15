import abc

from spacegame.hw05.hw05 import MovableAdapter, MoveCmd, UObject
from spacegame.hw08.hw08 import MacroCmd
from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC


class Generator:
    def get(self, key):
        pass


class Disposable(abc.ABC):
    @abc.abstractmethod
    def __del__(self):
        pass


class UObjectImpl(UObject, Disposable):
    def __init__(self, pool):
        super().__init__()
        self._pool = pool

    def __del__(self):
        # TODO: clear properties of object (del or clear 'position' and etc)
        self.store = {}
        self._pool.release(self)


class ReusablePool:
    def __init__(self, size):
        self._pool = [UObjectImpl(self) for _ in range(size)]

    def get(self):
        item = self._pool.pop()
        return item

    def release(self, item):
        self._pool.append(item)


def some_func():
    pool = ReusablePool(100)
    IoC.resolve(
        "IoC.register",
        "spaceships_pool",
        lambda *args: pool,
    ).execute()


def use_uobject():
    some_func()
    IoC.resolve(
        "IoC.register",
        "spaceship",
        lambda *args: IoC.resolve("spaceships_pool").get(),
    ).execute()
    print(len(IoC.resolve("spaceships_pool")._pool))
    spaceship = IoC.resolve("spaceship")
    print(len(IoC.resolve("spaceships_pool")._pool))
    # del spaceship
    # some_func()
    # print(len(IoC.resolve("spaceships_pool")._pool))


if __name__ == "__main__":
    InitScopeBasedIoCImplementationCmd().execute()

    some_func()
    print(len(IoC.resolve("spaceships_pool")._pool))

    starship = IoC.resolve("spaceships_pool").get()
    print(len(IoC.resolve("spaceships_pool")._pool))

    starship.hihi = 123
    starship.set_property("hihi", 321)

    del starship
    print(len(IoC.resolve("spaceships_pool")._pool))

    print(IoC.resolve("spaceships_pool")._pool[-1].hihi)
    print(IoC.resolve("spaceships_pool")._pool[-1].get_property("hihi"))


# if __name__ == "__main__":
#     InitScopeBasedIoCImplementationCmd().execute()

#     use_uobject()
#     print(len(IoC.resolve("spaceships_pool")._pool))
