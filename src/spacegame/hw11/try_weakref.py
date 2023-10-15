import weakref


class Object:
    def __init__(self):
        pass


class ObjectPool:
    def __init__(self):
        self._pool = weakref.WeakValueDictionary()
        self._id_as_counter = 0

    def get(self):
        key = str(self._counter)
        obj = None
        if key in self._pool:
            obj = self._pool[key]()
        else:
            obj = self._pool[key] = Object()
            self._id_as_counter += 1
        return obj


if __name__ == "__main__":
    pool = ObjectPool()
    print(pool._pool.data)

    obj0 = pool.get()
    print(pool._pool.data)

    # Объект obj1 удаляется из пула, когда он выходит из зоны видимости
    del obj0
    print(pool._pool.data)

    # Если запросить объект с тем же ключом снова, он будет создан заново
    obj1 = pool.get()
    obj2 = pool.get()
    print(pool._pool.data)

    print(pool._counter)
