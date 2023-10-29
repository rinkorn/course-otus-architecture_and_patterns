import abc
from time import sleep

from spacegame.hw09.hw09 import IoC
from spacegame.hw14.hw14 import HardStopCmd, SoftStopCmd


class IQueueFinisher(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass


class QueueFinisher(IQueueFinisher):
    """Завершальщик очереди"""

    def __init__(self, *args):
        self.stop_cmds = args
        # конечный автомат
        st0 = QueueFinisherState0(None)
        st1 = QueueFinisherState1(None)
        self.initial = st0

    def run(self):
        state = self.initial
        while state:
            state = state.handle()


class IState(abc.ABC):
    @abc.abstractmethod
    def set_next_state(self):
        pass

    @abc.abstractmethod
    def handle(self):
        pass


class QueueFinisherState0(IState):
    def __init__(self, stop_cmd):
        self.stop_cmd = stop_cmd

    def set_next_state(self, state):
        self.next_state = state

    def handle(self):
        print(self.__class__.__name__)
        sleep(1)
        # return IoC.resolve("signal.get", self)
        return self.next_state


class QueueFinisherState1(IState):
    def __init__(self, stop_cmd):
        self.stop_cmd = stop_cmd

    def set_next_state(self, state):
        self.next_state = state

    def handle(self):
        print(self.__class__.__name__)
        sleep(1)
        # return IoC.resolve("signal.get", self)
        return self.next_state


if __name__ == "__main__":
    stop_cmds = [
        SoftStopCmd,
        HardStopCmd,
    ]
    tf = QueueFinisher(stop_cmds)
    tf.run()
