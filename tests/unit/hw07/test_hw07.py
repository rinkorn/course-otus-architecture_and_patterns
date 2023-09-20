# %%
from queue import Queue

from spacegame.hw05.hw05 import (
    ICommand,
    MovableAdapter,
    MoveCmd,
    RotableAdapter,
    RotateCmd,
    UObject,
    Vector,
)
from spacegame.hw07.hw07 import (
    BaseAppException,
    DoubleRepeateCmd,
    ExceptionHandler,
    HelloWorldPrintCmd,
    IExceptionHandler,
    IQueue,
    LogPrintCmd,
    LogWriteCmd,
    RepeateCmd,
    SpecialErrorRaiserCmd,
)


def test_ExceptionHandler_0():
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()


def test_ExceptionHandler_1():
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()


def test_ExceptionHandler_2():
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()


def test_ExceptionHandler_3():
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()


def test_ExceptionHandler_4():
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()


def test_ExceptionHandler_5():
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()


def test_ExceptionHandler_6():
    spaceship = UObject()
    # spaceship.set_property("position", Vector([0.0, 0.0]))
    spaceship.set_property("position", Vector([None, 0.0]))
    spaceship.set_property("velocity", Vector([1.0, 1.0]))
    spaceship.set_property("direction", 0)
    spaceship.set_property("direction_numbers", 8)
    spaceship.set_property("angular_velocity", 1)

    print("Before:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()

    queue = Queue()
    queue.put(MoveCmd(MovableAdapter(spaceship)))
    queue.put(SpecialErrorRaiserCmd(BaseAppException))
    queue.put(RotateCmd(RotableAdapter(spaceship)))

    # handler = LogPrinterExcHandler(queue)
    # handler = RepeaterExcHandler(queue)
    # handler = DoubleRepeaterExcHandler(queue)
    handler = ExceptionHandler()
    handler.setup(
        MoveCmd,
        TypeError,
        # lambda cmd, exc: queue.put(HelloWorldPrintCmd()),
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )
    handler.setup(
        SpecialErrorRaiserCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(DoubleRepeateCmd(cmd)),
    )
    handler.setup(
        DoubleRepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(RepeateCmd(cmd)),
    )
    handler.setup(
        RepeateCmd,
        BaseAppException,
        lambda cmd, exc: queue.put(LogPrintCmd(cmd, exc)),
    )

    while True and not queue.empty():
        cmd = queue.get()
        try:
            cmd.execute()
        except Exception as e:
            exc = type(e)
            handler.handle(cmd, exc)
            ## ExceptionHandler.handle(cmd, exc).execute()
            ## IoC.resolve("ExceptionHandler", cmd, exc).execute()

    print("After:")
    print(f"position: {spaceship.get_property('position')}")
    print(f"direction: {spaceship.get_property('direction')}")
    print()
