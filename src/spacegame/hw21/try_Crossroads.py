import abc
from time import sleep

from spacegame.hw09.hw09 import IoC


class IState(abc.ABC):
    @abc.abstractmethod
    def next(self):
        pass


class TrafficLight:
    """Тоже можно было представить конечным автоматом, но для
    простоты восприятия состояний для перекретска этот класс
    упростили.
    """

    def green(self):
        pass

    def yellow(self):
        pass

    def red(self):
        pass

    def flashing_yellow(self):
        pass

    def switch_off(self):
        pass


class Crossroads:
    """Это дорожный перекресток"""

    def __init__(self, *args):
        self.traffic_lights = args

        # состояния светофоров на перекретске
        # 2ое состояние повторяется, т.к. из 2го можно перейти
        # как в 1 так и в 3
        st1: CrossroadsState1 = CrossroadsState1(*self.traffic_lights)
        st21: CrossroadsState2 = CrossroadsState2(*self.traffic_lights)
        st22: CrossroadsState2 = CrossroadsState2(*self.traffic_lights)
        st3: CrossroadsState3 = CrossroadsState3(*self.traffic_lights)

        st1.set_state(st21)  # st1 -> st2
        st21.set_state(st3)  # st2 -> st3
        st3.set_state(st22)  # st3 -> st2
        st22.set_state(st1)  # st2 -> st1
        self.initial = st1

    def run(self):
        next_state = self.initial
        while next_state:
            prev_name = next_state.__class__.__name__
            next_state = next_state.next()
            next_name = next_state.__class__.__name__
            print(f"{prev_name} --> {next_name}")
            sleep(2)


class CrossroadsState1(IState):
    def __init__(self, *args):
        self.traffic_lights = args

    def set_state(self, to):
        self.to = to

    def next(self):
        self.traffic_lights[0].green()
        self.traffic_lights[1].red()
        self.traffic_lights[2].red()
        self.traffic_lights[3].green()
        # return IoC.resolve("signal.get"", self)
        return self.to


class CrossroadsState2(IState):
    def __init__(self, *args):
        self.traffic_lights = args

    def set_state(self, to):
        self.to = to

    def next(self):
        self.traffic_lights[0].yellow()
        self.traffic_lights[1].yellow()
        self.traffic_lights[2].yellow()
        self.traffic_lights[3].yellow()
        return self.to


class CrossroadsState3(IState):
    def __init__(self, *args):
        self.traffic_lights = args

    def set_state(self, to):
        self.to = to

    def next(self):
        self.traffic_lights[0].red()
        self.traffic_lights[1].green()
        self.traffic_lights[2].green()
        self.traffic_lights[3].red()
        return self.to


class CrossroadsState4(IState):
    def __init__(self, *args):
        self.traffic_lights = args

    def set_state(self, to):
        self.to = to

    def next(self):
        self.traffic_lights[0].flashing_yellow()
        self.traffic_lights[1].flashing_yellow()
        self.traffic_lights[2].flashing_yellow()
        self.traffic_lights[3].flashing_yellow()
        return self.to


class CrossroadsState5(IState):
    def __init__(self, *args):
        self.traffic_lights = args

    def set_state(self, to):
        self.to = to

    def next(self):
        self.traffic_lights[0].switch_off()
        self.traffic_lights[1].switch_off()
        self.traffic_lights[2].switch_off()
        self.traffic_lights[3].switch_off()

        return self.to


if __name__ == "__main__":
    tl1 = TrafficLight()
    tl2 = TrafficLight()
    tl3 = TrafficLight()
    tl4 = TrafficLight()
    cr = Crossroads(tl1, tl2, tl3, tl4)
    cr.run()
