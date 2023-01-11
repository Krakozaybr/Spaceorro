from abc import ABC, abstractmethod
from typing import Union, Tuple

from pymunk import Vec2d
from pygame import Surface

from src.entities.modifiers_and_characteristics import LifeCharacteristics


class HealthBar(ABC):
    pos: Vec2d
    w: float
    h: float
    color: Union[str, Tuple[int, int, int]]

    @abstractmethod
    def render(
        self, screen: Surface, life_characteristics: LifeCharacteristics, pos: Vec2d
    ):
        pass
