from abc import abstractmethod, ABCMeta
from src.abstract import RenderUpdateObject


class Scene(RenderUpdateObject, metaclass=ABCMeta):

    @abstractmethod
    def catch_event(self, e):
        pass
