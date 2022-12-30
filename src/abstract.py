from abc import abstractmethod, ABC
from typing import Dict

from pygame import Surface
import json


class Serializable(ABC):
    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict):
        pass

    def serialize(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def deserialize(cls, data: str):
        return cls.from_dict(json.loads(data))


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
