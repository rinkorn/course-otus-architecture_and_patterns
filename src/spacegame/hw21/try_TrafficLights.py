import abc
from time import sleep

from spacegame.hw09.hw09 import IoC


class IState(abc.ABC):
    @abc.abstractmethod
    def set_state(self):
        pass

    @abc.abstractmethod
    def next(self):
        pass


class TrafficLight:
    """Это светофор"""

    def __init__(self, *args):
        self.colors = args
        # конечный автомат
        st0 = TrafficLightState0(*self.colors)  # power_off
        st1 = TrafficLightState1(*self.colors)  # red
        st21 = TrafficLightState2(*self.colors)  # yellow
        st22 = TrafficLightState2(*self.colors)  # yellow
        st3 = TrafficLightState3(*self.colors)  # green
        st5 = TrafficLightState5(*self.colors)  # flashing_green
        st0.set_state(st1)  # power_off --> red
        st1.set_state(st21)  # red --> yellow
        st21.set_state(st3)  # yellow --> green
        st3.set_state(st5)  # green -> flashing_green
        st5.set_state(st22)  # flashing_green -> yellow
        st22.set_state(st1)  # yellow -> red
        self.initial = st0

    def run(self):
        state = self.initial
        while state:
            state = state.next()


class TrafficLightState0(IState):
    def __init__(self, *args):
        self.colors = args

    def set_state(self, to):
        self.to = to

    def next(self):
        print("power_off")
        sleep(0.1)
        # return IoC.resolve("signal.get", self)
        return self.to


class TrafficLightState1(IState):
    def __init__(self, *args):
        self.colors = args

    def set_state(self, to):
        self.to = to

    def next(self):
        print(self.colors[0])
        sleep(5)
        # return IoC.resolve("signal.get", self)
        return self.to


class TrafficLightState2(IState):
    def __init__(self, *args):
        self.colors = args

    def set_state(self, to):
        self.to = to

    def next(self):
        print(self.colors[1])
        sleep(1.5)
        return self.to


class TrafficLightState3(IState):
    def __init__(self, *args):
        self.colors = args

    def set_state(self, to):
        self.to = to

    def next(self):
        print(self.colors[2])
        sleep(5)
        return self.to


class TrafficLightState4(IState):
    def __init__(self, *args):
        self.colors = args

    def set_state(self, to):
        self.to = to

    def next(self):
        print(f"{self.colors[0]}+{self.colors[1]}")
        sleep(1)
        return self.to


class TrafficLightState5(IState):
    def __init__(self, *args):
        self.colors = args

    def set_state(self, to):
        self.to = to

    def next(self):
        print(f"flashing_{self.colors[2]}...")
        sleep(1)
        return self.to


if __name__ == "__main__":
    colors = ("red", "yellow", "green")
    tf = TrafficLight(*colors)
    tf.run()
