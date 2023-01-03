from typing import List

from pymunk import Vec2d

from src.entities.abstract.abstract import Entity
from src.environment.abstract import Environment
from src.map.abstract import EntityRegistrator
from src.map.impls import BasicMap


class BasicEnvironment(Environment):

    map_impl: BasicMap

    def __init__(self, map_impl: BasicMap):
        self.map_impl = map_impl

    def get_entity_registrator(self) -> EntityRegistrator:
        return self.map_impl

    def get_entities_near(self, pos: Vec2d, radius: float) -> List[Entity]:
        return self.map_impl.get_entities_near(pos, radius)
