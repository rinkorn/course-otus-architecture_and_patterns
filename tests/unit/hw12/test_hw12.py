import inspect

import pytest
from spacegame.hw05.hw05 import IMovable, IRotable, UObject, Vector
from spacegame.hw09.hw09 import InitScopeBasedIoCImplementationCmd, IoC
from spacegame.hw12.hw12 import (
    Adapter,
    MoveCmdPluginCmd,
    RotateCmdPluginCmd,
)

# Реализованы тесты на генератор адаптеров


@pytest.fixture(scope="function")
def initialization():
    InitScopeBasedIoCImplementationCmd().execute()
    IoC.resolve(
        "scopes.current.set",
        IoC.resolve(
            "scopes.new",
            IoC.resolve("scopes.root"),
        ),
    ).execute()
    MoveCmdPluginCmd().execute()
    RotateCmdPluginCmd().execute()


def test_adapter_register(initialization):
    # assign
    # action
    IoC.resolve(
        "IoC.register",
        "Adapter",
        lambda *args: Adapter.generate(args[0])(args[1]),
    ).execute()


def test_adapter_unregister(initialization):
    # assign
    IoC.resolve(
        "IoC.register",
        "Adapter",
        lambda *args: Adapter.generate(args[0])(args[1]),
    ).execute()
    # action
    IoC.resolve("IoC.unregister", "Adapter").execute()


def test_adapter_generate_class_name(initialization):
    # assign
    obj = UObject()
    obj.set_property("position", Vector([12.0, 5.0]))
    obj.set_property("velocity", Vector([-7.0, 3.0]))
    obj.set_property("direction", 0)
    obj.set_property("direction_numbers", 8)
    obj.set_property("angular_velocity", -1)
    # action
    MovableAdapter = Adapter.generate(IMovable)(obj)
    RotableAdapter = Adapter.generate(IRotable)(obj)
    # assert
    assert MovableAdapter.__class__.__name__ == "AutoGeneratedMovableAdapter"
    assert RotableAdapter.__class__.__name__ == "AutoGeneratedRotableAdapter"


def test_adapter_generate_attributes(initialization):
    # assign
    obj = UObject()
    # action
    MovableAdapter = Adapter.generate(IMovable)(obj)
    attr_names_imovable = [
        m[0] for m in inspect.getmembers(IMovable, inspect.isfunction)
    ]
    attr_names_movadapt = [
        m[0] for m in inspect.getmembers(MovableAdapter, inspect.isfunction)
    ]
    # assert
    # assert set(attr_names_imovable) == set(attr_names_movadapt)
    assert all(name in attr_names_imovable for name in attr_names_movadapt)


def test_adapter_get(initialization):
    # assign
    IoC.resolve(
        "IoC.register",
        "Adapter",
        lambda *args: Adapter.generate(args[0])(args[1]),
    ).execute()
    obj = UObject()
    obj.set_property("position", Vector([12.0, 5.0]))
    obj.set_property("velocity", Vector([-7.0, 3.0]))
    # action
    movable_obj = IoC.resolve("Adapter", IMovable, obj)
    # assert
    assert movable_obj.get_position() == Vector([12.0, 5.0])
    assert movable_obj.get_velocity() == Vector([-7.0, 3.0])


def test_adapter_set(initialization):
    # assign
    IoC.resolve(
        "IoC.register",
        "Adapter",
        lambda *args: Adapter.generate(args[0])(args[1]),
    ).execute()
    obj = UObject()
    obj.set_property("position", Vector([12.0, 5.0]))
    obj.set_property("velocity", Vector([-7.0, 3.0]))
    # action
    movable_obj = IoC.resolve("Adapter", IMovable, obj)
    movable_obj.get_position() == Vector([12.0, 5.0])
    movable_obj.set_position(Vector([123, 321]))
    # assert
    assert movable_obj.get_position() == Vector([123, 321])
