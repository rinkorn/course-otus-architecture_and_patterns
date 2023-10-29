import queue
import threading


def worker(q):
    while True:
        item = q.get()  # Блокируется до появления элемента в очереди
        # Выполнение операций с элементом
        print(f"Обработан элемент: {item}")
        q.task_done()  # Помечаем элемент как обработанный


# Создание очереди
my_queue = queue.Queue()

# Создание и запуск потока
my_thread = threading.Thread(target=worker, args=(my_queue,), daemon=True)
my_thread.start()

# Добавление элементов в очередь
for i in range(10):
    my_queue.put(i)

# # # Дождемся завершения потока
my_queue.join()
# my_thread.join()
