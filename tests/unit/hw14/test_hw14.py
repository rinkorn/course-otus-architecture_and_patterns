import threading

from spacegame.hw07.hw07 import DoNothingCmd
from spacegame.hw09.hw09 import Dictionary
from spacegame.hw14.hw14 import (
    EventSetterCmd,
    HardStopCmd,
    HardStoppableAdapter,
    InitProcessorContextCmd,
    Processable,
    Processor,
    SoftStopCmd,
    SoftStoppableAdapter,
)


def test_HardStopCmd_should_stop_processor_immediately():
    # assign
    obj = Dictionary()
    InitProcessorContextCmd(obj).execute()
    queue = obj["queue"]
    queue.put(DoNothingCmd())
    queue.put(HardStopCmd(HardStoppableAdapter(obj)))
    queue.put(DoNothingCmd())
    # action
    processor = Processor(Processable(obj))
    processor.wait()
    # assert
    assert queue.qsize() == 1


def test_SoftStopCmd_should_stop_processor_when_queue_is_empty():
    # assign
    obj = Dictionary()
    InitProcessorContextCmd(obj).execute()
    queue = obj["queue"]
    queue.put(DoNothingCmd())
    queue.put(SoftStopCmd(SoftStoppableAdapter(obj)))
    queue.put(DoNothingCmd())
    # action
    processor = Processor(Processable(obj))
    processor.wait()
    # assert
    assert queue.empty()


def test_SoftStopCmd_should_stop_processor_when_queue_is_empty_with_event_setter():
    # assign
    obj = Dictionary()
    InitProcessorContextCmd(obj).execute()
    event = threading.Event()
    queue = obj["queue"]
    queue.put(DoNothingCmd())
    queue.put(SoftStopCmd(SoftStoppableAdapter(obj)))
    queue.put(DoNothingCmd())
    queue.put(EventSetterCmd(event))
    # action
    processor = Processor(Processable(obj))
    while not event.is_set():
        pass
    processor.wait()
    # assert
    assert queue.empty()
