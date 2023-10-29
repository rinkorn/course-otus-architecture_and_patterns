import abc
import threading

from spacegame.hw05.hw05 import ICommand
from spacegame.hw07.hw07 import DoNothingCmd
from spacegame.hw09.hw09 import Dictionary, IDictionary, IoC
from spacegame.hw14.hw14 import BlockingCollection


class IReceiver(abc.ABC):
    pass


class ServerThread:
    _stop: bool = False
    _thread: threading.Thread = None
    _receiver: IReceiver = None

    def __init__(self, receiver: IReceiver):
        ServerThread._receiver = receiver

    @staticmethod
    def _action():
        cmd = ServerThread._receiver.receive()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            try:
                # handler.handle(cmd, exc)
                # ExceptionHandler.handle(cmd, exc).execute()
                # IoC.resolve("ExceptionHandler", cmd, exc).execute()
                print(f"Error! {exc} in {type(cmd)}")
            except Exception as e:
                print(f"Fatal error! {exc} in {type(cmd)}")

    def start(self):
        def loop():
            while not ServerThread._stop:
                ServerThread._action()

        thread = threading.Thread(loop)
        thread.start()


class HardStopCmd(ICommand):
    def __init__(self, thread: ServerThread):
        self._thread = thread

    def execute(self):
        # if threading.current_thread().ident != self._thread._thread.ident:
        if threading.current_thread() != self._thread._thread:
            raise Exception()
        self._thread.stop = True


class SoftStopCmd(ICommand):
    def __init__(self, thread: ServerThread):
        self._thread = thread

    def execute(self):
        old = self._thread._action

        def empty():
            self._thread.stop = True

        def not_empty():
            old()

        def action():
            self._thread._receiver.empty(empty)
            self._thread._receiver.not_empty(not_empty)

        self._thread._action = action


class InitCmd(ICommand):
    def __init__(self, context: IDictionary):
        self._context = context

    def execute(self):
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

        self._context.__setitem__("can_continue", True)
        self._context.__setitem__("queue", queue)
        self._context.__setitem__("process", process)


# %%
# if __name__ == "__main__":
#     queue = BlockingCollection(100)
#     receiver = ReceiverAdapter()
#     IoC.resolve("Sender.01")
#     IoC.resolve("HardStopCmd", thread)
#     sender = SenderAdapter(queue)
#     thread = ServerThread(receiver)
#     thread.start()
#     sender.send(HardStopCmd(thread))
