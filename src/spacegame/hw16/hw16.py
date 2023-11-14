# %%
import queue
import uuid

from spacegame.hw05.hw05 import ICommand
from spacegame.hw07.hw07 import IQueue
from spacegame.hw09.hw09 import Dictionary, IoC
from spacegame.hw14.try_ServerThread import IReceiver


class StopCmd(ICommand):
    def __init__(self, stop):
        self.stop = stop

    def execute(self):
        self.stop = True


class LambdaCmd(ICommand):
    def __init__(self, action: callable):
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

    def empty(self):
        return self._queue.empty()


class GameCmd(ICommand):
    def __init__(self, parent_scope: str, init_game_cmd_names: list):
        # очередь игры не обязательно потокобезопасная, т.к.
        # игра уже лежит в потокобезопасной очереди
        # self._queue = queue.Queue()
        receiver = IoC.resolve("IReceiver")

        self._game_scope = IoC.resolve("scopes.new", parent_scope)
        IoC.resolve("scopes.current.set", self._game_scope).execute()
        # sngleton object receiver
        IoC.resolve("IoC.register", "queue", lambda *args: receiver).execute()

        game_objects = Dictionary()
        IoC.resolve(
            "IoC.register", "game_objects", lambda *args: game_objects
        ).execute()
        players: int = IoC.resolve("Players")
        spaceships: int = IoC.resolve("Spaceships")
        for i_p in range(players):
            for i_s in range(spaceships):
                spaceship = IoC.resolve("Spaceship")
                for name in init_game_cmd_names:
                    IoC.resolve(name, spaceship).execute()
                # IoC.resolve(
                #     "Spaceship.label_and_add", spaceship, game_objects
                # ).execute()
                # IoC.resolve("Spaceship.assign_to", spaceship, player).execute()
                # IoC.resolve("Spaceship.locate", spaceship).execute()

    def execute(self):
        IoC.resolve("scopes.current.set", self._game_scope).execute()
        recevier: IReceiver = IoC.resolve("queue")
        cmd = recevier.receive()
        cmd.execute()


if __name__ == "__main__":
    # RepeatableCmd(GameCmd('parent_scope', ["label_and_add", 'locate'])
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
