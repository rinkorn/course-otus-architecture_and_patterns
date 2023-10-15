import os
import threading
import time

local_data = threading.local()


def test(i):
    local_data.value = f"Data from Thread {i}"
    thread = threading.current_thread()
    print(f"Current Thread Name: {thread.name}")
    print(f"Current thread Id:{threading.get_ident()}")
    time.sleep(2)
    print(f"Done..{i}")


if __name__ == "__main__":
    threads = []
    for i in range(0, 2):
        thread = threading.Thread(
            target=test,
            name=f"Thread {i}",
            args=[i],
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
