import threading

# Создаем объект ThreadLocal
local_data = threading.local()

# Словарь для хранения данных по идентификатору потока
threads_data = {}

print(f"Thread global: {threading.get_ident()}")
print()


# Функция для работы в потоке 1
def thread_function1():
    local_data.value = "Data from Thread 1"
    current_thread = threading.current_thread()
    # thread_id = threading.get_ident()
    thread_id = threading.get_native_id()
    threads_data[thread_id] = local_data.value
    print(f"Thread 1 name {current_thread.name}: {local_data.value}")
    print(f"Thread 1 id {thread_id}: {local_data.value}")
    print(local_data.__dict__)
    print()


# Функция для работы в потоке 2
def thread_function2():
    local_data.value = "Data from Thread 2"
    current_thread = threading.current_thread()
    # thread_id = threading.get_ident()
    thread_id = threading.get_native_id()
    threads_data[thread_id] = local_data.value
    print(f"Thread 2 name {current_thread.name}: {local_data.value}")
    print(f"Thread 2 id {thread_id}: {local_data.value}")
    print(local_data.__dict__)
    print()


# Создаем два потока с указанием имен
thread1 = threading.Thread(target=thread_function1, name="Thread-1")
thread2 = threading.Thread(target=thread_function2, name="Thread-2")

# Запускаем потоки
thread1.start()
thread2.start()

# Ожидаем завершения потоков
thread1.join()
thread2.join()

print(threads_data)
