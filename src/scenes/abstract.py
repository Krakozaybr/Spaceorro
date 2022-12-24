from abc import abstractmethod, ABCMeta


class Scene(metaclass=ABCMeta):
    @abstractmethod
    def render(self, screen):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def catch_event(self, e):
        pass
