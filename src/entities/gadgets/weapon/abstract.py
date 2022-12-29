from abc import ABC, abstractmethod

from pymunk import Vec2d

from src.entities.characteristics import WeaponCharacteristics


class Weapon(ABC):

    characteristics: WeaponCharacteristics

    @abstractmethod
    def shoot(self, pos: Vec2d) -> bool:
        pass
