from abc import ABC, abstractmethod
from typing import Union, Tuple

from pymunk import Vec2d
from pygame import Surface


class HealthBar(ABC):
    pos: Vec2d
    w: float
    h: float
    color: Union[str, Tuple[int, int, int]]

    @abstractmethod
    def render(self, screen: Surface, health: float, pos: Vec2d):
        pass
