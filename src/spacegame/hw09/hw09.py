import abc
import threading
from collections import defaultdict

from spacegame.hw05.hw05 import ICommand


# %%
class IDictionary(abc.ABC):
    """В качестве ключа - зависимость, в качестве значения - стратегия(по
    входным параметрам возвратит ссылку на нужный объект)"""

    @abc.abstractmethod
    def __getitem__(self, key: str):
        pass

    @abc.abstractmethod
    def __setitem__(self, key: str, value: callable):
        pass

    @abc.abstractmethod
    def __contains__(self, key: str):
        pass

    @abc.abstractmethod
    def __delitem__(sefl, key: str):
        pass


class Dictionary(IDictionary):
    def __init__(self):
        self._store = {}

    def __getitem__(self, key: str):
        return self._store[key]

    def __setitem__(self, key: str, value: callable):
        self._store[key] = value

    def __contains__(self, key: str):
        return key in self._store.keys()

    def __delitem__(self, key: str):
        del self._store[key]


class ThreadSafeDictionary(IDictionary):
    def __init__(self):
        self._store = {}

    def __getitem__(self, key: str):
        with threading.Lock():
            return self._store.get(key)

    def __setitem__(self, key: str, value: callable):
        with threading.Lock():
            self._store[key] = value

    def __contains__(self, key: str):
        with threading.Lock():
            return key in self._store

    def __delitem__(self, key: str):
        with threading.Lock():
            del self._store[key]


ConcurrentDictionary = ThreadSafeDictionary


# %%
class IThreadLocal:
    @abc.abstractmethod
    def __getitem__(self):
        pass

    @abc.abstractmethod
    def __setitem__(self):
        pass

    @abc.abstractmethod
    def __contains__(self):
        pass


class ThreadLocal(IThreadLocal):
    def __init__(self):
        self._store = threading.local()

    def __getitem__(self, key: str):
        value = None
        if key in self:
            value = self._store.__getattribute__(key)
        return value

    def __setitem__(self, key: str, value: any):
        self._store.__setattr__(key, value)

    def __contains__(self, key):
        return key in self._store.__dict__.keys()


class ThreadLocal2(IThreadLocal):
    def __init__(self):
        self._store = defaultdict(dict)

    def __getitem__(self, key: str):
        thread_id = ThreadLocal._get_thread_id()
        if key not in self._store[thread_id]:
            return None
        return self._store[thread_id][key]

    def __setitem__(self, key: str, value: any):
        thread_id = ThreadLocal._get_thread_id()
        self._store[thread_id][key] = value

    def __contains__(self, key):
        thread_id = ThreadLocal._get_thread_id()
        return key in self._store[thread_id]

    @staticmethod
    def _get_thread_id():
        return threading.get_native_id()


# %%
class IScope(abc.ABC):
    @abc.abstractmethod
    def resolve(key: str, *args: any):
        pass


class _Scope(IScope):
    """
    dependencies - словарик, где в виде ключа - зависимость, а в виде значения -
    стратегия (по входным параметрам возвратит ссылку на нужный объект)
    Не поток устанавливается в scope, а scope устанавливается в потоке.
    """

    def __init__(self, dependencies: IDictionary, parent: IScope):
        self.dependencies = dependencies
        self.parent = parent

    def resolve(self, key: str, *args: any):
        if key in self.dependencies:
            strategy = self.dependencies[key]
            return strategy(*args)
        else:
            return self.parent.resolve(key, *args)


class LeafScope(IScope):
    def __init__(self, strategy: callable):
        self._strategy = strategy

    def resolve(self, key: str, *args: any):
        return self._strategy(key, *args)


# %%
class IoCException(Exception):
    pass


class _SetupStrategyCmd(ICommand):
    def __init__(self, new_strategy):
        self.new_strategy = new_strategy

    def execute(self):
        IoC._strategy = self.new_strategy


class IIoC(abc.ABC):
    @abc.abstractstaticmethod
    def resolve(key: str, *args: any):
        pass

    @abc.abstractstaticmethod
    def _default_strategy(key: str, *args: any):
        pass

    @abc.abstractproperty
    def _strategy():
        pass


class IoC(IIoC):
    @staticmethod
    def resolve(key: str, *args: any):
        return IoC._strategy(key, *args)

    @staticmethod
    def _default_strategy(key: str, *args: any):
        """Если нужно будет заменить именно дефолтную стратегию (то есть убрать
        возможность делать "IoC.setup_strategy", то вернём ссылку
        на IoC._default_strategy, чтобы где-то как-то её подменить или удалить.
        """
        if key == "IoC.setup_strategy":
            strategy = args[0]
            return _SetupStrategyCmd(strategy)
        elif key == "IoC.default_strategy":
            return IoC._default_strategy
        else:
            raise ValueError(
                f"Unknown IoC dependency key {key}. "
                f"Make sure that {key} has been registered"
            )

    _strategy: callable = _default_strategy


# %%
class IStrategy(abc.ABC):
    @abc.abstractstaticmethod
    def resolve(self, key: str, *args: any):
        pass


class ScopeBasedResolveDependencyStrategy(IStrategy):
    _root: _Scope = None
    _current_scopes = ThreadLocal()

    @staticmethod
    def _default_scope(*args):
        return ScopeBasedResolveDependencyStrategy._root

    @staticmethod
    def resolve(key: str, *args: any):
        # if key == "IoC.setup_strategy":
        #     return SetupStrategyCmd(args[0])
        if key == "scopes.root":
            return ScopeBasedResolveDependencyStrategy._root
        else:
            # Не поток устанавливается в scope, а scope устанавливается в потоке.
            scope = ScopeBasedResolveDependencyStrategy._current_scopes["value"]
            if scope is None:
                scope = ScopeBasedResolveDependencyStrategy._default_scope()
            return scope.resolve(key, *args)


# %%
class InitSingleThreadScopeCmd(ICommand):
    def execute(self) -> None:
        IoC.resolve(
            "IoC.register",
            "scopes.storage",
            lambda *args: Dictionary(),
        ).execute()


def RegisterIoCDependencyException(Exception):
    pass


def UnregisterIoCDependencyException(Exception):
    pass


class _RegisterIoCDependencyCmd(ICommand):
    def __init__(self, key: str, strategy: callable):
        self.key = key
        self.strategy = strategy

    def execute(self):
        try:
            current_scope = ScopeBasedResolveDependencyStrategy._current_scopes["value"]
            current_scope.dependencies.__setitem__(self.key, self.strategy)
        except BaseException as e:
            raise RegisterIoCDependencyException("Can't register dependency")


class _UnregisterIoCDependencyCmd(ICommand):
    def __init__(self, key: str):
        self.key = key

    def execute(self):
        try:
            current_scope = ScopeBasedResolveDependencyStrategy._current_scopes["value"]
            current_scope.dependencies.__delitem__(self.key)
        except BaseException as e:
            raise UnregisterIoCDependencyException("Can't unregister dependency")


class _SetScopeInCurrentThreadCmd(ICommand):
    def __init__(self, scope):
        self.scope = scope

    def execute(self):
        ScopeBasedResolveDependencyStrategy._current_scopes.__setitem__(
            "value",
            self.scope,
        )


class InitScopeBasedIoCImplementationCmd(ICommand):
    def execute(self):
        if ScopeBasedResolveDependencyStrategy._root is not None:
            return

        dependencies = ConcurrentDictionary()

        # scopes.storage - словарик для всех scopes, которые есть в приложении
        dependencies.__setitem__(
            "scopes.storage",
            lambda *args: ConcurrentDictionary(),
        )

        # scopes.new - команда, которая создаёт storage когда это необходимо
        dependencies.__setitem__(
            "scopes.new",
            lambda *args: _Scope(
                IoC.resolve("scopes.storage"),
                args[0],
            ),
        )

        # scopes.current - получить доступ к текущему scope
        current_scope = ScopeBasedResolveDependencyStrategy._current_scopes["value"]
        default_scope = ScopeBasedResolveDependencyStrategy._default_scope
        dependencies.__setitem__(
            "scopes.current",
            lambda *args: current_scope if current_scope is not None else default_scope,
        )

        # scopes.current - устанвоить scope в текущем потоке
        dependencies.__setitem__(
            "scopes.current.set",
            lambda *args: _SetScopeInCurrentThreadCmd(args[0]),
        )

        dependencies.__setitem__(
            "IoC.register",
            lambda *args: _RegisterIoCDependencyCmd(args[0], args[1]),
        )

        dependencies.__setitem__(
            "IoC.unregister",
            lambda *args: _UnregisterIoCDependencyCmd(args[0]),
        )

        root_scope = _Scope(
            dependencies,
            LeafScope(IoC.resolve("IoC.default_strategy")),
            # parent=None,
        )

        ScopeBasedResolveDependencyStrategy._root = root_scope

        IoC.resolve(
            "IoC.setup_strategy",
            ScopeBasedResolveDependencyStrategy.resolve,
        ).execute()

        _SetScopeInCurrentThreadCmd(root_scope).execute()


if __name__ == "__main__":
    InitScopeBasedIoCImplementationCmd().execute()
    # InitSingleThreadScopeCmd().execute()


if __name__ == "__main__":
    gameID123 = IoC.resolve(
        "scopes.new",
        IoC.resolve("scopes.root"),
    )
    IoC.resolve(
        "scopes.current.set",
        gameID123,
    )

    IoC.resolve(
        "IoC.register",
        "a",
        lambda *args: f"just a! and params: {args}",
    ).execute()

    print(IoC.resolve("a", 123, 456))

    IoC.resolve(
        "IoC.unregister",
        "a",
    ).execute()

# %%
if __name__ == "__main__":
    scope = IoC.resolve("scopes.new", IoC.resolve("scopes.root"))
    IoC.resolve("scopes.current.set", scope).execute()
    IoC.resolve(
        "IoC.register",
        "dependency",
        lambda *args: 1,
    ).execute()
    IoC.resolve("dependency") == 1

    scope = IoC.resolve("scopes.new", IoC.resolve("scopes.root"))
    IoC.resolve("scopes.current.set", scope).execute()
    IoC.resolve(
        "IoC.register",
        "dependency",
        lambda *args: 1,
    ).execute()
    IoC.resolve("dependency") == 1
