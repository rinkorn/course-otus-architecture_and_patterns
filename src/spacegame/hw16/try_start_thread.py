import threading
from ast import arg

from spacegame.hw05.hw05 import ICommand
from spacegame.hw07.hw07 import IQueue
from spacegame.hw09.hw09 import Dictionary, InitScopeBasedIoCImplementationCmd, IoC
from spacegame.hw14.hw14 import BlockingCollection, HardStopCmd
from spacegame.hw14.try_ServerThread import IReceiver


class StopThreadCmd(ICommand):
    def __init__(self, can_continue):
        self.can_continue = can_continue

    def execute(self):
        self.can_continue = False


class PutToQueueCmd(ICommand):
    def __init__(self, queue: IQueue, cmd: ICommand):
        self.queue = queue
        self.cmd = cmd

    def execute(self):
        self.queue.put(self.cmd)


class LambdaCmd(ICommand):
    def __init__(self, action: callable):
        self.action = action

    def execute(self):
        self.action()


class StartThreadCmd(ICommand):
    def __init__(self, thread_name):
        self.thread_name = thread_name
        self.can_continue: bool = True
        self.queue: IQueue = BlockingCollection(100)

        def evaluation():
            while self.can_continue:
                print(self.can_continue)
                cmd = self.queue.get()
                print(self.can_continue)
                try:
                    cmd.execute()
                    print(f"Executed: {cmd.__class__.__name__}")
                except Exception as e:
                    exc = type(e)
                    try:
                        # handler.handle(cmd, exc)
                        # ExceptionHandler.handle(cmd, exc).execute()
                        # IoC.resolve("ExceptionHandler", cmd, exc).execute()
                        print(f"Error! {exc} in {cmd.__class__.__name__}")
                    except Exception as e:
                        print(f"Fatal error! {exc} in {cmd.__class__.__name__}")

        self.thread = threading.Thread(
            target=evaluation,
            daemon=True,
        )
        self.thread.start()

    def execute(self):
        IoC.resolve(
            "IoC.register",
            self.thread_name,
            lambda *args: self.thread,
        ).execute()
        IoC.resolve(
            "IoC.register",
            self.thread_name + ".queue",
            lambda *args: self.queue,
        ).execute()
        IoC.resolve(
            "IoC.register",
            self.thread_name + ".stop",
            lambda *args: StopThreadCmd(self.can_continue),
        ).execute()
        IoC.resolve(
            "IoC.register",
            self.thread_name + ".put",
            lambda *args: PutToQueueCmd(self.queue, args[0]),
        ).execute()


# %%
if __name__ == "__main__":
    InitScopeBasedIoCImplementationCmd().execute()

    IoC.resolve(
        "IoC.register",
        "Thread.start",
        lambda *args: StartThreadCmd(args[0]),
    ).execute()

    # запустить поток (обычно потоки не в пуле, т.к. запускаются
    # на длительный срок)
    IoC.resolve("Thread.start", "thread_id123").execute()

    # остановить поток
    cmd = IoC.resolve("thread_id123.stop")
    IoC.resolve("thread_id123.put", cmd).execute()


# %%
# if __name__ == "__main__":
#     # Функция для добавления элемента в очередь
#     def add_to_queue(item):
#         # Добавляем элемент в очередь
#         q.put(item)

#     # Функция для получения элемента из очереди
#     def get_from_queue():
#         # Получаем элементы из очереди
#         while True:
#             item = q.get()
#             if not item:
#                 break
#             print(item)

#     # Запускаем две функции параллельно
#     add_thread = threading.Thread(target=add_to_queue, args=(10,))
#     add_thread.start()
#     get_thread = threading.Thread(target=get_from_queue)
#     get_thread.start()

#     # Ждем завершения обеих функций
#     add_thread.join()
#     get_thread.join()
