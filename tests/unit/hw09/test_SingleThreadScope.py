import pytest
from spacegame.hw09.hw09 import (
    Dictionary,
    InitScopeBasedIoCImplementationCmd,
    InitSingleThreadScopeCmd,
    IoC,
)


@pytest.fixture(scope="function")
def SingleThreadScopeTests():
    InitScopeBasedIoCImplementationCmd().execute()
    # create thread safe scope as root(base scope)
    scope = IoC.resolve("scopes.new", IoC.resolve("scopes.root"))
    IoC.resolve("scopes.current.set", scope).execute()
    # setup not thread safe scopes (saving resources)
    InitSingleThreadScopeCmd().execute()


def test_create_new_scope(SingleThreadScopeTests):
    IoC.resolve("scopes.new", IoC.resolve("scopes.root"))


def test_scopes_storage_is_dictionary(SingleThreadScopeTests):
    assert isinstance(IoC.resolve("scopes.storage"), Dictionary)
