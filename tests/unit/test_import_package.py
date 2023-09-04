def test_import_package():
    try:
        import spacegame
    except ModuleNotFoundError:
        assert False, "Can't import target package."
