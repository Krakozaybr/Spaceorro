from abc import abstractmethod, ABC
from typing import List, Tuple, Set

from pygame import Surface
from pymunk.vec2d import Vec2d

from src.abstract import RenderUpdateObject, Serializable
from src.entities.abstract.abstract import Entity
from src.scenes.game.camera import Camera


class AbstractCluster(Serializable, RenderUpdateObject, ABC):
    entities: Set[Entity]
    pos: Tuple[int, int]

    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def add_entity(self, entity: Entity):
        pass

    @abstractmethod
    def remove_entity(self, entity: Entity):
        pass


class AbstractClustersStore(Serializable, ABC):
    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def keys(self) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def values(self) -> List[AbstractCluster]:
        pass

    @abstractmethod
    def __contains__(self, item):
        pass


class AbstractMapGenerator(ABC):
    @abstractmethod
    def generate_clusters(
        self, x, y, clusters: AbstractClustersStore
    ) -> List[AbstractCluster]:
        ...


class EntityRegistrator(ABC):
    @abstractmethod
    def add_entity(self, entity: Entity):
        pass


class AbstractMap(Serializable, EntityRegistrator, ABC):
    clusters: AbstractClustersStore
    map_generator: AbstractMapGenerator

    @abstractmethod
    def render_at(self, screen: Surface, camera: Camera, pos: Vec2d):
        pass

    @abstractmethod
    def update_at(self, pos: Vec2d, dt: float):
        pass

    @abstractmethod
    def remove_entity(self, entity: Entity):
        pass

    def contains_entity(self, entity: Entity):
        return entity in self.clusters
