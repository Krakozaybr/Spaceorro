from abc import abstractmethod, ABCMeta
from typing import List
from src.entities.abstract import Entity


# TODO implement these
class AbstractCluster(metaclass=ABCMeta):
    entities: List[Entity]


class AbstractMap(metaclass=ABCMeta):
    clusters: List[List[AbstractCluster]]


class AbstractMapGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate_cluster(self) -> AbstractCluster:
        ...
