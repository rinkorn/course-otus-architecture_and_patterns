# %%
import queue

from spacegame.hw05.hw05 import ICommand
from spacegame.hw07.hw07 import IQueue
from spacegame.hw09.hw09 import IoC


class StopCmd(ICommand):
    def __init__(self, stop):
        self.stop = stop

    def execute(self):
        self.stop = True


class LambdaCmd(ICommand):
    def __init__(self, action):
        self.action = action

    def execute(self):
        self.action()


class ConcurrentQueue(IQueue):
    def __init__(self, maxsize: int):
        """Должна быть потокобезопасной!!!"""
        self._queue = queue.Queue(maxsize)

    def put(self, item):
        self._queue.put(item)

    def get(self):
        # операция должна выполняться блокируемым образом
        # это значит, что если в очереди не будет каких-либо
        # сообщений, то в месте queue.get() поток блокируется
        # до тех пор пока сообщение не появится в очереди
        return self._queue.get()
        # while not self._queue.empty():
        #     yield self._queue.get()

    def empty(self):
        return self._queue.empty()


class GameCmd(ICommand):
    def __init__(self, id: str):
        # очередь игры не обязательно потокобезопасная, т.к.
        # игра уже лежит в потокобезопасной очереди
        self._queue = queue.Queue()
        self._id = id
        IoC.resolve("scopes.new", id).execute()
        IoC.resolve("scopes.current", id).execute()
        # IoC.resolve(
        #     "IoC.register",
        #     "queue",
        #     lambda *args: self._queue,
        # ).execute()
        IoC.resolve(
            "IoC.register",
            "put",
            lambda *args: self._queue.put(args[0]),
        ).execute()

    def execute(self):
        IoC.resolve("scopes.current", self._id).execute()
        cmd = self._queue.get()
        cmd.execute()


def start_thread(*args):
    stop: bool = False
    q: IQueue = ConcurrentQueue(100)

    name = args[0]
    IoC.resolve(
        "IoC.register",
        name + ".stop",
        lambda *args: StopCmd(True),
    ).execute()
    IoC.resolve(
        "IoC.register",
        name + ".put",
        lambda *args: LambdaCmd(lambda: queue.put(args[0])),
    ).execute()

    while (not stop) and not q.empty():
        cmd = q.get()
        try:
            cmd.execute()
            print(f"Executed: {cmd}")
        except Exception as e:
            exc = type(e)
            try:
                # handler.handle(cmd, exc)
                # ExceptionHandler.handle(cmd, exc).execute()
                IoC.resolve("ExceptionHandler", cmd, exc).execute()
                print(f"Error! {exc} in {type(cmd)}")
            except Exception as e:
                print(f"Fatal error! {exc} in {type(cmd)}")


# %%
if __name__ == "__main__":

    def func():
        stop = True

    LambdaCmd(func).execute()

    # зарегестрировать зависимость старта потока
    IoC.resolve(
        "IoC.register",
        "Thread.start",
        start_thread,
    )

    # запустить поток (обычно потоки не в пуле, т.к. запускаются
    # на длительный срок)
    IoC.resolve("Thread.start", "id123").execute()

    # остановить поток
    cmd = IoC.resolve("id123.stop")
    IoC.resolve("id123.queue").put(cmd)
    # или
    IoC.resolve("id123.queue", cmd).execute()


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
