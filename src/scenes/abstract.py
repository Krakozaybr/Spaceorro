from abc import abstractmethod, ABC
from src.abstract import Updateable


class Scene(Updateable, ABC):
    @abstractmethod
    def render(self, screen):
        pass

    @abstractmethod
    def catch_event(self, e):
        pass
