import abc
import datetime as dt
from collections import defaultdict
from collections.abc import Callable
from queue import Queue

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


# %%
class IExceptionHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self):
        pass


# %%
class IQueue(abc.ABC):
    @abc.abstractmethod
    def put(self, item):
        pass

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def empty(self):
        pass


# %%
class DoNothingCmd(ICommand):
    def execute(self):
        pass


class HelloWorldPrintCmd(ICommand):
    def __init__(self):
        self.msg = "Hello World!"

    def execute(self):
        print(self.msg)


class SpecialErrorRaiserCmd(ICommand):
    def __init__(self, exception: Exception = Exception):
        self.exception = exception

    def execute(self):
        Error = self.exception
        raise Error("Raise an error manually.")


# %%
class LogPrintCmd(ICommand):
    def __init__(self, cmd, exc):
        self.cmd = cmd
        self.exc = exc

    def execute(self):
        print(
            f"Time: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"
            f"Command: {self.cmd.__class__.__name__}.\n"
            f"Exception: {self.exc.__name__}.\n"
            f"\n"
        )


class LogWriteCmd(ICommand):
    def __init__(self, cmd, exc):
        self.cmd = cmd
        self.exc = exc

    def execute(self):
        with open("log.txt", "a") as file:
            file.write(
                f"Time: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"
                f"Command: {self.cmd.__class__.__name__}.\n"
                f"Exception: {self.exc.__name__}.\n"
                f"\n"
            )


class RepeateCmd(ICommand):
    def __init__(self, cmd: ICommand):
        self.cmd = cmd

    def execute(self):
        self.cmd.execute()


class DoubleRepeateCmd(ICommand):
    def __init__(self, cmd: ICommand):
        self.cmd = cmd

    def execute(self):
        self.cmd.execute()


# %%
class LogPrinterExcHandler(IExceptionHandler):
    def __init__(self, queue: IQueue):
        self.queue = queue

    def handle(self, cmd: ICommand, exc: Exception):
        self.queue.put(LogPrintCmd(cmd, exc))


class LogWriterExcHandler(IExceptionHandler):
    def __init__(self, queue: IQueue):
        self.queue = queue

    def handle(self, cmd: ICommand, exc: Exception):
        self.queue.put(LogWriteCmd(exc))


class RepeaterExcHandler(IExceptionHandler):
    def __init__(self, queue: IQueue):
        self.queue = queue

    def handle(self, cmd: ICommand, exc: Exception):
        if not isinstance(cmd, RepeateCmd):
            self.queue.put(RepeateCmd(cmd))
        else:
            self.queue.put(LogWriteCmd(cmd, exc))


class DoubleRepeaterExcHandler(IExceptionHandler):
    def __init__(self, queue):
        self.queue = queue
        self.store = {}

    def handle(self, cmd: ICommand, exc: Exception):
        key = (cmd.__class__.__name__, exc.__name__)

        if not isinstance(cmd, RepeateCmd | DoubleRepeateCmd):
            self.queue.put(RepeateCmd(cmd))
            return

        if not isinstance(cmd, DoubleRepeateCmd):
            self.queue.put(DoubleRepeateCmd(cmd))
            return


class OldExceptionHandler(IExceptionHandler):
    def __init__(self):
        self.store = {}

    def setup(self, cmd: ICommand, exc: Exception, lambda_func: Callable):
        # cmd: Move,
        # exc: ValueError,
        # (cmd, exc) => queue.put(LogPrinterCmd(cmd, exc))
        key = (cmd.__name__, exc.__name__)
        self.store[key] = lambda_func

    def handle(self, cmd: ICommand, exc: Exception):
        key = (cmd.__class__.__name__, exc.__name__)
        lambda_func = self.store[key]
        lambda_func(cmd, exc)


class ExceptionHandler(IExceptionHandler):
    def __init__(self):
        self.store = defaultdict(dict)

    def setup(self, cmd: ICommand, exc: Exception, lambda_func: Callable):
        # cmd: Move,
        # exc: ValueError,
        # (cmd, exc) => queue.put(LogPrinterCmd(cmd, exc))
        cmd_key = cmd.__name__
        exc_key = exc.__name__
        self.store[cmd_key][exc_key] = lambda_func

    def handle(self, cmd: ICommand, exc: Exception):
        cmd_key = cmd.__class__.__name__
        exc_key = exc.__name__
        lambda_func = self.store[cmd_key][exc_key]
        lambda_func(cmd, exc)


# %%
if __name__ == "__main__":
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()
