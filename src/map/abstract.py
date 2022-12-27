from abc import abstractmethod, ABC
from typing import List
from src.entities.abstract import Entity
from src.abstract import RenderUpdateObject, Serializable


# TODO implement these
class AbstractCluster(Serializable, RenderUpdateObject, ABC):
    entities: List[Entity]


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
    def generate_clusters(self, x, y, clusters) -> List[AbstractCluster]:
        ...


class AbstractMap(Serializable, ABC):
    clusters: AbstractClustersStore
    map_generator: AbstractMapGenerator

    @abstractmethod
    def render_at(self, x, y):
        pass

    @abstractmethod
    def update_at(self, x, y):
        pass
