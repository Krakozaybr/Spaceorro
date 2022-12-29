from abc import abstractmethod, ABC
from src.abstract import Updateable
from pygame import Surface


class Scene(Updateable, ABC):
    @abstractmethod
    def render(self, screen: Surface):
        pass
