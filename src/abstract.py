from abc import abstractmethod, ABCMeta


class Serializable(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(data: str):
        pass


class Updateable(metaclass=ABCMeta):
    @abstractmethod
    def update(self, dt):
        pass


class Renderable(metaclass=ABCMeta):
    @abstractmethod
    def render(self, screen, camera):
        pass


class RenderUpdateObject(Renderable, Updateable, metaclass=ABCMeta):
    pass
