import abc
from time import sleep

from spacegame.hw09.hw09 import IoC


# %%
class IStateMachine(abc.ABC):
    @abc.abstractmethod
    def run(self):
        pass


class TrafficLightStateMachine(IStateMachine):
    """Это светофор"""

    def __init__(self, *args):
        self.colors = args
        # конечный автомат
        st0 = TrafficLightState0(self.colors)  # power_off
        st1 = TrafficLightState1(*self.colors)  # red
        st21 = TrafficLightState2(*self.colors)  # yellow
        st22 = TrafficLightState2(*self.colors)  # yellow
        st3 = TrafficLightState3(*self.colors)  # green
        st5 = TrafficLightState5(*self.colors)  # flashing_green
        st0.to(st1)  # power_off --> red
        st1.to(st21)  # red --> yellow
        st21.to(st3)  # yellow --> green
        st3.to(st5)  # green -> flashing_green
        st5.to(st22)  # flashing_green -> yellow
        st22.to(st1)  # yellow -> red
        self.initial_state = st0

    def run(self):
        state = self.initial_state
        while state:
            state = state.change()


# %%
class IState(abc.ABC):
    @abc.abstractmethod
    def to(self):
        pass

    @abc.abstractmethod
    def change(self):
        pass


class TrafficLightState0(IState):
    def __init__(self, *args):
        self.colors = args

    def to(self, state):
        self.next_state = state

    def change(self):
        print("power_off")
        sleep(0.1)
        # return IoC.resolve("signal.get", self)
        return self.next_state


class TrafficLightState1(IState):
    def __init__(self, *args):
        self.colors = args

    def to(self, state):
        self.next_state = state

    def change(self):
        self.colors["red"]()
        sleep(5)
        # return IoC.resolve("signal.get", self)
        return self.next_state


class TrafficLightState2(IState):
    def __init__(self, *args):
        self.colors = args

    def to(self, state):
        self.next_state = state

    def change(self):
        color = self.colors["yellow"]()
        print(color)
        sleep(1.5)
        return self.next_state


class TrafficLightState3(IState):
    def __init__(self, *args):
        self.colors = args

    def to(self, state):
        self.next_state = state

    def change(self):
        color = self.colors["green"]()
        print(color)
        sleep(5)
        return self.next_state


class TrafficLightState4(IState):
    def __init__(self, *args):
        self.colors = args

    def to(self, state):
        self.next_state = state

    def change(self):
        r_color = self.colors["red"]()
        y_color = self.colors["yellow"]()
        print(f"{self.colors[0]}+{self.colors[1]}")
        sleep(1)
        return self.next_state


class TrafficLightState5(IState):
    def __init__(self, *args):
        self.colors = args

    def to(self, state):
        self.next_state = state

    def change(self):
        print(f"flashing_{self.colors['green']()}...")
        sleep(1)
        return self.next_state


if __name__ == "__main__":
    colors = {}
    colors["red"] = lambda *args: "red"
    colors["yellow"] = lambda *args: "yellow"
    colors["green"] = lambda *args: "green"
    TrafficLightStateMachine(colors).run()
