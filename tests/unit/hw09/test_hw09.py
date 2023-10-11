import pytest


def import_and_init_IoC():
    from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC

    InitScopeBasedIoCImplementationCmd().execute()
    return IoC


def test_root_scope_is_available():
    IoC = import_and_init_IoC()
    assert IoC.resolve("scopes.root") is not None
    IoC.resolve("IoC.register", "a", lambda *args: 123).execute()
    del IoC


def test_create_scope_is_possible_at_any_moment():
    IoC = import_and_init_IoC()
    parent_scope = IoC.resolve("scopes.root")
    assert IoC.resolve("scopes.new", parent_scope) is not None
    assert IoC.resolve("a") == 123
    del IoC
