from typing import Callable

from src.abstract import Updateable


class Timer(Updateable):
    def __init__(self, max_time: float, *listeners: Callable):
        self.time = 0
        self.max_time = max_time
        self.listeners = list(listeners)

    def update(self, dt: float):
        self.time += dt
        if self.time > self.max_time:
            self.time = self.time % self.max_time
            for listener in self.listeners:
                listener()

    def add_listener(self, listener: Callable):
        self.listeners.append(listener)

    def remove_listener(self, listener: Callable):
        self.listeners.remove(listener)
