import abc
from collections import defaultdict
from queue import Queue
from typing import Any

from spacegame.hw05.hw05 import (
    ICommand,
    MovableAdapter,
    MoveCmd,
    RotableAdapter,
    RotateCmd,
    UObject,
    Vector,
)


# %%
class BaseAppException(Exception):
    pass


class EmptyCmd(ICommand):
    def __init__(self):
        pass

    def execute(self):
        pass


# %%
class IQueue(abc.ABC):
    @abc.abstractmethod
    def put(self, other):
        pass

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def empty(self):
        pass


# %%
class IExceptionHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self):
        pass


class ExceptionHandler(IExceptionHandler):
    def __init__(self, queue: IQueue):
        self.queue = queue
        c = self.cmd_default = EmptyCmd()
        e = self.exc_default = BaseAppException()
        self.store = defaultdict(dict)
        self.store[str(type(c))][str(type(e))] = EmptyCmd()

    def handle(self, command: ICommand, exception: Exception):
        cmd_str = str(type(command))
        exc_str = str(type(exception))
        exc_getted = self.store.get(cmd_str, self.store[self.cmd_default])
        cmd_getted = exc_getted.get(exc_str, self.exc_default)
        self.queue.put(cmd_getted)


# %%
def main(queue):
    exception_handler = ExceptionHandler(queue)
    while not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as exc:
            exception_handler.handle(cmd, exc)
            # ExceptionHandler.handle(cmd, exc).execute()
            # IoC.resolve("ExceptionHandler", cmd, exc).execute()


if __name__ == "__main__":
    spaceship = UObject()
    spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    # spaceship.set_property("velocity", [1.0, 1.0])
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", -1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue(maxsize=0)
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(RotateCmd(RotableAdapter(spaceship)))
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(RotateCmd(RotableAdapter(spaceship)))
    main(queue)

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()
