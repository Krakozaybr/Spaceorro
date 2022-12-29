from abc import abstractmethod, ABC

from pygame import Surface


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(data: str):
        pass


class Updateable(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass


class Renderable(ABC):
    @abstractmethod
    def render(self, screen: Surface, camera):
        pass


class RenderUpdateObject(Renderable, Updateable, ABC):
    pass
