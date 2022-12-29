from abc import abstractmethod, ABC
from typing import List, Tuple

from pygame import Surface
from pymunk.vec2d import Vec2d

from src.abstract import RenderUpdateObject, Serializable
from src.entities.abstract import Entity
from src.scenes.game.camera import Camera


class AbstractCluster(Serializable, RenderUpdateObject, ABC):
    entities: List[Entity]
    pos: Tuple[int, int]


class AbstractClustersStore(Serializable, ABC):
    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def values(self):
        pass


class AbstractMapGenerator(ABC):
    @abstractmethod
    def generate_clusters(
        self, x, y, clusters: AbstractClustersStore
    ) -> List[AbstractCluster]:
        ...


class AbstractMap(Serializable, ABC):
    clusters: AbstractClustersStore
    map_generator: AbstractMapGenerator

    @abstractmethod
    def render_at(self, screen: Surface, camera: Camera, pos: Vec2d):
        pass

    @abstractmethod
    def update_at(self, pos: Vec2d, dt: float):
        pass
