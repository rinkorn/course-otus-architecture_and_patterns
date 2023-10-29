import queue
import threading
import time


def worker(q):
    while True:
        try:
            item = q.get(block=True, timeout=1)  # Попытка получить элемент из очереди
            # Выполнение операций с элементом
            print(f"Обработан элемент: {item}")
            q.task_done()  # Помечаем элемент как обработанный
        except queue.Empty:
            print("Очередь пуста. Поток засыпает на некоторое время.")
            time.sleep(2)  # Засыпаем на некоторое время, чтобы не нагружать процессор
            continue


# Создание очереди
my_queue = queue.Queue()

# Создание и запуск потока
my_thread = threading.Thread(target=worker, args=(my_queue,))
my_thread.start()

# Добавление элементов в очередь
for i in range(10):
    my_queue.put(i)

# Дождемся завершения потока
my_queue.join()
my_thread.join()
