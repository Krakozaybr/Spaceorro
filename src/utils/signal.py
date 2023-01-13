from typing import List, Callable

from src.utils.all_annotations import all_annotations


class Signal:
    listeners: List[Callable]

    def __init__(self):
        self.listeners = []

    def emit(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

    def connect(self, listener: Callable):
        self.listeners.append(listener)

    def remove(self, listener: Callable):
        self.listeners.remove(listener)


class SignalMixin:
    def __init__(self):
        for field_name, cls in all_annotations(self.__class__).items():
            if not hasattr(self, field_name) and cls == Signal:
                setattr(self, field_name, cls())