from abc import abstractmethod, ABC


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
    def update(self, dt):
        pass


class Renderable(ABC):
    @abstractmethod
    def render(self, screen, camera):
        pass


class RenderUpdateObject(Renderable, Updateable, ABC):
    pass
