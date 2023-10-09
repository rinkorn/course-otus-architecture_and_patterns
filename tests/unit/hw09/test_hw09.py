from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC


def test_root_scope_is_available():
    InitScopeBasedIoCImplementationCmd().execute()
    assert IoC.resolve("scopes.root") is not None


def test_create_scope_is_possible_at_any_moment():
    InitScopeBasedIoCImplementationCmd().execute()
    assert IoC.resolve("scopes.new", IoC.resolve("scopes.root")) is not None
