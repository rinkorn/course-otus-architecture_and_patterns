import threading

from spacegame.hw07.hw07 import DoNothingCmd
from spacegame.hw14.hw14 import (
    ContextDictionary,
    EventLoop,
    EventSetterCmd,
    HardStopCmd,
    InitEventLoopContextCmd,
    SoftStopCmd,
)


def test_HardStopCmd_should_stop_processor_immediately():
    # assign
    processor_context = ContextDictionary()
    InitEventLoopContextCmd(processor_context).execute()
    # event = threading.Event()
    queue = processor_context["queue"]
    queue.put(DoNothingCmd())
    queue.put(HardStopCmd(processor_context))
    queue.put(DoNothingCmd())
    # action
    processor = EventLoop(processor_context)
    processor.wait()
    # while not event.is_set():
    #     pass
    # assert
    assert queue.qsize() == 1


def test_SoftStopCmd_should_stop_processor_when_queue_is_empty():
    # assign
    processor_context = ContextDictionary()
    InitEventLoopContextCmd(processor_context).execute()
    event = threading.Event()
    queue = processor_context["queue"]
    queue.put(DoNothingCmd())
    queue.put(SoftStopCmd(processor_context))
    queue.put(DoNothingCmd())
    queue.put(EventSetterCmd(event))
    # action
    processor = EventLoop(processor_context)
    # processor.wait()
    while not event.is_set():
        pass
    # assert
    assert queue.empty()
