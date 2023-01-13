from abc import abstractmethod, ABC
from typing import List

from pymunk import Vec2d

from src.entities.abstract.abstract import Entity
from src.map.abstract import EntityRegistrator


class Environment(ABC):

    impl = None

    @abstractmethod
    def get_entity_registrator(self) -> EntityRegistrator:
        pass

    @abstractmethod
    def get_entities_near(self, pos: Vec2d, radius: float) -> List[Entity]:
        pass

    @abstractmethod
    def get_entity_at(self, pos: Vec2d):
        pass


impl: Environment


def get_environment() -> Environment:
    return impl


def set_environment(new_impl):
    global impl
    assert isinstance(new_impl, Environment)
    impl = new_impl
