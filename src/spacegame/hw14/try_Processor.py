import abc
import threading

from spacegame.hw05.hw05 import ICommand
from spacegame.hw07.hw07 import DoNothingCmd
from spacegame.hw09.hw09 import Dictionary, IDictionary
from spacegame.hw14.hw14 import BlockingCollection


class IProcessable(abc.ABC):
    @abc.abstractmethod
    def can_continue(self):
        pass

    @abc.abstractmethod
    def process(self):
        pass


class Processable(IProcessable):
    def __init__(self, context: IDictionary):
        self.context = context

    def can_continue(self):
        return self.context["can_continue"]

    def process(self):
        process = self.context["process"]
        process()


class Processor:
    def __init__(self, context: IProcessable):
        self.processable = context
        self.thread = threading.Thread(target=self.evaluation)
        self.thread.start()

    def wait(self):
        # можем навечно заблокироваться в этом join;
        # на такие случаи надо добавить time-outы
        self.thread.join()

    def evaluation(self):
        while self.processable.can_continue():
            self.processable.process()


class InitCmd(ICommand):
    def __init__(self, context: IDictionary):
        self.context = context

    def execute(self):
        can_continue = True
        queue = BlockingCollection()

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

        self.context["can_continue"] = can_continue
        self.context["queue"] = queue
        self.context["process"] = process


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


def test_HardStopCmd_Should_Stop_Processor_Immediately():
    # assign
    processor_context = Dictionary()
    InitCmd(processor_context).execute()
    queue = processor_context["queue"]
    queue.put(DoNothingCmd())
    queue.put(HardStopCmd(processor_context))
    queue.put(DoNothingCmd())
    # action
    processor = Processor(Processable(processor_context))
    processor.wait()
    # assert
    assert queue.qsize() == 1


def test_SoftStopCmd_Should_Stop_Processor_When_Queue_Is_Empty():
    # assign
    processor_context = Dictionary()
    InitCmd(processor_context).execute()
    queue = processor_context["queue"]
    queue.put(DoNothingCmd())
    queue.put(SoftStopCmd(processor_context))
    queue.put(DoNothingCmd())
    # action
    processor = Processor(Processable(processor_context))
    processor.wait()
    # assert
    assert queue.empty()


# %%
if __name__ == "__main__":
    test_HardStopCmd_Should_Stop_Processor_Immediately()
    test_SoftStopCmd_Should_Stop_Processor_When_Queue_Is_Empty()
