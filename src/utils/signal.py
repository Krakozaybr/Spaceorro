from typing import List, Callable

from src.utils.all_annotations import all_annotations


class Signal:
    listeners: List[Callable]

    def __init__(self):
        self.listeners = []

    def emit(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.emit(*args, **kwargs)

    def connect(self, listener: Callable):
        self.listeners.append(listener)

    def remove(self, listener: Callable):
        self.listeners.remove(listener)

    def clear(self):
        self.listeners.clear()


class SignalAnnotationMixin:
    def __init__(self):
        for field_name, cls in all_annotations(self.__class__).items():
            if not hasattr(self, field_name) and cls == Signal:
                setattr(self, field_name, cls())


class SignalFieldMixin:

    _signals = []
    _are_signals_inited: bool

    def __init__(self):
        if not hasattr(self, '_are_signals_inited'):
            for signal_name in self._signals:
                setattr(self, signal_name, Signal())
            self._are_signals_inited = True


    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls._signals: List[str]

        if not hasattr(cls, "_signals"):
            cls._signals = []
        else:
            cls._signals = cls._signals.copy()
        for field_name, value in cls.__dict__.items():
            if isinstance(value, Signal):
                cls._signals.append(field_name)
