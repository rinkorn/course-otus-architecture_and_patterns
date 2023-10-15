import os
import threading
import time

from spacegame.hw09.hw09 import (
    InitScopeBasedIoCImplementationCmd,
    IoC,
)

InitScopeBasedIoCImplementationCmd().execute()


def main(i):
    root_scope = IoC.resolve("scopes.root")
    print(root_scope)
    IoC.resolve(
        "scopes.new",
        root_scope,
    )
    # IoC.resolve(
    #     "scopes.current.set",
    #     root_scope,
    # )
    # IoC.resolve(
    #     "IoC.register",
    #     "a",
    #     lambda *args: f"HELLO a! {i}",
    # ).execute()
    time.sleep(0.2)
    print(f"Done..{i}")


if __name__ == "__main__":
    threads = []
    for i in range(0, 2):
        thread = threading.Thread(
            target=main,
            name=f"Thread {i}",
            args=[i],
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
