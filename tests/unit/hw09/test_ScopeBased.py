import pytest
from spacegame.hw09.hw09 import (
    InitScopeBasedIoCImplementationCmd,
    InitSingleThreadScopeCmd,
    IoC,
)


@pytest.fixture(scope="function")
def ScopeBasedTests():
    InitScopeBasedIoCImplementationCmd().execute()


def test_root_scope_is_available(ScopeBasedTests):
    root_scope = IoC.resolve("scopes.root")
    assert root_scope is not None


def test_create_scope_is_possible_at_any_moment(ScopeBasedTests):
    scope = IoC.resolve(
        "scopes.new",
        IoC.resolve("scopes.root"),
    )
    assert scope is not None


def test_registered_dependency_should_handle_resolve_request_with_dependency_name(
    ScopeBasedTests,
):
    IoC.resolve(
        "scopes.current.set",
        IoC.resolve("scopes.new", IoC.resolve("scopes.root")),
    ).execute()
    IoC.resolve(
        "IoC.register",
        "dependency",
        lambda *args: 1,
    ).execute()
    assert IoC.resolve("dependency") == 1


def test_registered_dependency_can_not_ber_redefined(ScopeBasedTests):
    scope = IoC.resolve("scopes.new", IoC.resolve("scopes.root"))
    IoC.resolve("scopes.current.set", scope).execute()
    IoC.resolve(
        "IoC.register",
        "dependency",
        lambda *args: 1,
    ).execute()
    assert IoC.resolve("dependency") == 1

    with pytest.raises(Exception):
        IoC.resolve(
            "IoC.register",
            "dependency",
            lambda *args: 2,
        ).execute()


def test_resolving_dependency_depends_on_current_scope(ScopeBasedTests):
    scope1 = IoC.resolve("scopes.new", IoC.resolve("scopes.root"))
    IoC.resolve("scopes.current.set", scope1).execute()
    IoC.resolve(
        "IoC.register",
        "dependency",
        lambda *args: 1,
    ).execute()
    assert IoC.resolve("dependency") == 1

    scope2 = IoC.resolve("scopes.new", IoC.resolve("scopes.root"))
    IoC.resolve("scopes.current.set", scope2).execute()
    IoC.resolve(
        "IoC.register",
        "dependency",
        lambda *args: 2,
    ).execute()
    assert IoC.resolve("dependency") == 2

    IoC.resolve("scopes.current.set", scope1).execute()
    assert IoC.resolve("dependency") == 1


def test_resolving_dependency_depends_on_scope_hierarchy(ScopeBasedTests):
    scope1 = IoC.resolve("scopes.new", IoC.resolve("scopes.root"))
    IoC.resolve("scopes.current.set", scope1).execute()
    IoC.resolve(
        "IoC.register",
        "dependency1",
        lambda *args: 1,
    ).execute()
    assert IoC.resolve("dependency1") == 1
    with pytest.raises(Exception):
        IoC.resolve("dependency2")

    scope2 = IoC.resolve("scopes.new", scope1)
    IoC.resolve("scopes.current.set", scope2).execute()
    IoC.resolve(
        "IoC.register",
        "dependency2",
        lambda *args: 1,
    ).execute()
    assert IoC.resolve("dependency1") == 1
    assert IoC.resolve("dependency2") == 1

    IoC.resolve("scopes.current.set", scope1).execute()

    assert IoC.resolve("dependency1", 1)
    with pytest.raises(Exception):
        IoC.resolve("dependency2")
