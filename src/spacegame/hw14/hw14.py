import abc
import threading
from queue import Queue

from spacegame.hw05.hw05 import ICommand
from spacegame.hw07.hw07 import DoNothingCmd, IQueue
from spacegame.hw09.hw09 import Dictionary, IDictionary


# %%
class BlockingCollection(IQueue):
    """Должна быть потокобезопасной, т.е. put and get в очередь
    можно из разных потоков блокируемым способом.
    После take очередь заснёт.
    """

    def __init__(self, maxsize=0):
        self._queue = Queue(maxsize)

    def put(self, item):
        self._queue.put(item)

    def get(self):
        return self._queue.get()

    def empty(self):
        return self._queue.empty()

    def qsize(self):
        return self._queue.qsize()


class NonBlockingCollection(IQueue):
    """Не потокобезопасная, т.к. это очередь самой игры,
    которая и так будет находиться внутри потокобезопасного
    потока.
    """

    def __init__(self, maxsize=0):
        self._queue = Queue(maxsize)

    def put(self, item):
        self._queue.put(item)

    def get(self):
        return self._queue.get()

    def empty(self):
        return self._queue.empty()

    def qsize(self):
        return self._queue.qsize()


# %%
class IProcessable(abc.ABC):
    @abc.abstractmethod
    def can_continue(self):
        pass

    @abc.abstractmethod
    def thread_timeout(self):
        pass

    @abc.abstractmethod
    def process(self):
        pass


class Processable(IProcessable):
    def __init__(self, context: IDictionary):
        self.o = context

    def can_continue(self):
        return self.o["can_continue"]

    def thread_timeout(self):
        return self.o["thread_timeout"]

    def process(self):
        self.o["process"].__call__()


class Processor:
    def __init__(self, context: IProcessable):
        self.context = context
        self.thread = threading.Thread(
            target=self.evaluation,
            daemon=True,
        )
        self.thread.start()

    def wait(self):
        self.thread.join(
            timeout=self.context.thread_timeout(),
        )

    def evaluation(self):
        while self.context.can_continue():
            self.context.process()


class InitProcessorContextCmd(ICommand):
    def __init__(self, context: IDictionary):
        self.o = context

    def execute(self):
        queue = BlockingCollection()

        def process():
            cmd = queue.get()
            try:
                cmd.execute()
                print(f"Executed: {cmd.__class__.__name__}")
            except Exception as e:
                exc = type(e)
                try:
                    # handler.handle(cmd, exc)
                    # ExceptionHandler.handle(cmd, exc).execute()
                    # IoC.resolve("ExceptionHandler", cmd, exc).execute()
                    print(f"Error! {exc} in {type(cmd)}")
                except Exception as e:
                    print(f"Fatal error! {exc} in {type(cmd)}")

        self.o["can_continue"] = True
        self.o["queue"] = queue
        self.o["process"] = process
        self.o["thread_timeout"] = 10


class IHardStoppable(abc.ABC):
    @abc.abstractmethod
    def set_can_continue(self, value):
        pass


class HardStoppableAdapter(IHardStoppable):
    def __init__(self, uobject: IDictionary):
        self.o = uobject

    def set_can_continue(self, value: bool):
        self.o.__setitem__("can_continue", value)


class HardStopCmd(ICommand):
    def __init__(self, context: IHardStoppable):
        self.o = context

    def execute(self):
        self.o.set_can_continue(False)


class ISoftStoppable(abc.ABC):
    @abc.abstractmethod
    def get_process(self):
        pass

    @abc.abstractmethod
    def set_process(self, value):
        pass

    @abc.abstractmethod
    def get_queue(self):
        pass

    @abc.abstractmethod
    def set_can_continue(self, value):
        pass


class SoftStoppableAdapter(ISoftStoppable):
    def __init__(self, context: IDictionary):
        self.o = context

    def get_process(self):
        return self.o.__getitem__("process")

    def set_process(self, value):
        self.o.__setitem__("process", value)

    def get_queue(self):
        return self.o.__getitem__("queue")

    def set_can_continue(self, value):
        self.o.__setitem__("can_continue", value)


class SoftStopCmd(ICommand):
    def __init__(self, context: ISoftStoppable):
        self.o = context

    def execute(self):
        previous_process = self.o.get_process()

        def process():
            previous_process()
            queue = self.o.get_queue()
            if queue.qsize() == 0:
                self.o.set_can_continue(False)

        self.o.set_process(process)


class EventSetterCmd(ICommand):
    def __init__(self, event: threading.Event):
        self.event = event

    def execute(self):
        self.event.set()


def test_HardStopCmd_Should_Stop_Processor_Immediately():
    # assign
    processor_context = Dictionary()
    InitProcessorContextCmd(processor_context).execute()
    queue = processor_context["queue"]
    queue.put(DoNothingCmd())
    queue.put(HardStopCmd(HardStoppableAdapter(processor_context)))
    queue.put(DoNothingCmd())
    # action
    processor = Processor(Processable(processor_context))
    processor.wait()
    # assert
    assert queue.qsize() == 1
    print("test passed")


def test_SoftStopCmd_Should_Stop_Processor_When_Queue_Is_Empty():
    # assign
    processor_context = Dictionary()
    InitProcessorContextCmd(processor_context).execute()
    queue = processor_context["queue"]
    queue.put(DoNothingCmd())
    queue.put(SoftStopCmd(SoftStoppableAdapter(processor_context)))
    queue.put(DoNothingCmd())
    # action
    processor = Processor(Processable(processor_context))
    processor.wait()
    # assert
    assert queue.empty()
    print("test passed")


# %%
if __name__ == "__main__":
    test_HardStopCmd_Should_Stop_Processor_Immediately()
    test_SoftStopCmd_Should_Stop_Processor_When_Queue_Is_Empty()
