import abc
import threading
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
from spacegame.hw07.hw07 import DoNothingCmd, IQueue
from spacegame.hw09.hw09 import Dictionary, IDictionary, IoC


class ContextDictionary(IDictionary):
    def __init__(self):
        self._store = {}

    def __getitem__(self, key: str):
        return self._store[key]

    def __setitem__(self, key: str, value: any):
        self._store[key] = value

    def __contains__(self, key: str):
        return key in self._store.keys()

    def __delitem__(self, key: str):
        del self._store[key]


class BlockingCollection(IQueue):
    """Должна быть потокобезопасной!!!"""

    def __init__(self, maxsize=0):
        self._queue = Queue(maxsize)

    def put(self, item, block=True, timeout=1):
        # self._queue.put(item, block=block, timeout=timeout)
        self._queue.put(item)

    def get(self):
        return self._queue.get()

    def empty(self):
        return self._queue.empty()

    def qsize(self):
        return self._queue.qsize()


class IEventLoop(abc.ABC):
    @abc.abstractmethod
    def __init__(self, queue: IQueue):
        pass

    @abc.abstractmethod
    def wait(self):
        pass


class ProcessStrategy:
    @staticmethod
    def process(context):
        queue = context["queue"]
        cmd = queue.get()
        try:
            cmd.execute()
            print(f"Executed: {cmd}")
        except Exception as e:
            exc = type(e)
            print(f"Error {exc} in {type(cmd)}")
            # handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()


class EventLoop(IEventLoop):
    # possible names: MyThread, ServerThread, EventLoop
    def __init__(self, context: IDictionary):
        self.context = context
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def wait(self):
        self.thread.join(timeout=self.context["thread_join_timeout"])

    def loop(self):
        while self.context["can_continue"]:
            cmd = self.context["queue"].get()
            try:
                cmd.execute()
                print(f"Executed: {cmd}")
            except Exception as e:
                exc = type(e)
                print(f"Error {exc} in {type(cmd)}")
                # handler.handle(cmd, exc)
                ## ExceptionHandler.handle(cmd, exc).execute()
                ## IoC.resolve("ExceptionHandler", cmd, exc).execute()


class InitEventLoopContextCmd(ICommand):
    def __init__(self, context: IDictionary):
        self.context = context

    def execute(self):
        def process():
            cmd = queue.get()
            try:
                cmd.execute()
                print(f"Executed: {cmd}")
            except Exception as e:
                exc = type(e)
                try:
                    # handler.handle(cmd, exc)
                    # ExceptionHandler.handle(cmd, exc).execute()
                    # IoC.resolve("ExceptionHandler", cmd, exc).execute()
                    print(f"Error! {exc} in {type(cmd)}")
                except Exception as e:
                    print(f"Fatal error! {exc} in {type(cmd)}")

        self.context["process"] = process
        self.context["can_continue"] = True
        self.context["queue"] = BlockingCollection()
        self.context["thread_join_timeout"] = 2


class HardStopCmd(ICommand):
    def __init__(self, context: IDictionary):
        self.context = context

    def execute(self):
        self.context["can_continue"] = False


class SoftStopCmd(ICommand):
    def __init__(self, context: IDictionary):
        self.context = context

    def execute(self):
        previous_process = self.context["process"]

        def process():
            previous_process()
            queue = self.context["queue"]
            if queue.qsize() == 0:
                self.context["can_continue"] = False

        self.context["process"] = process


class EventSetterCmd(ICommand):
    def __init__(self, event: threading.Event):
        self.event = event

    def execute(self):
        self.event.set()


# %%
if __name__ == "__main__":
    # test_EventLoopCanRead
    spaceship = UObject()
    spaceship.set_property("position", Vector([12.0, 5.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 5)

    # event = threading.Event()

    # pre
    context = ContextDictionary()
    InitEventLoopContextCmd(context).execute()

    queue = context["queue"]
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(RotateCmd(RotableAdapter(spaceship)))
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(RotateCmd(RotableAdapter(spaceship)))
    # queue.put(HardStopCmd(context))
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    # queue.put(EventSetterCmd(event))

    # act
    processor = EventLoop(context)
    # while not event.is_set():
    #     pass
    processor.wait()

    # post
    if queue.empty():
        print("queue is empty")
    assert queue.empty() is True

    print()
    print(spaceship.get_property("position"))
    print(spaceship.get_property("direction"))
