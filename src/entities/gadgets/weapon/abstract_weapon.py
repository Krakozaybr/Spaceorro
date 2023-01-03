from abc import ABC, abstractmethod

from pymunk import Vec2d

from src.abstract import Serializable, Updateable
from src.environment.abstract import get_environment
from src.map.abstract import EntityRegistrator


class AbstractStateWeapon(Serializable, Updateable, ABC):
    @abstractmethod
    def shoot(self, pos: Vec2d) -> bool:
        pass

    @property
    def entity_registrator(self) -> EntityRegistrator:
        return get_environment().get_entity_registrator()


# TODO unnecessary
# class PeriodicalWeapon(Weapon, ABC):
#     @abstractmethod
#     def shoot(self, dt: float, pos: Vec2d) -> bool:
#         pass
