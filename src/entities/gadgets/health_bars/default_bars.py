from abc import ABC
from typing import Tuple, Union

import pygame.draw
from pygame import Surface
from pymunk import Vec2d

from src.entities.abstract.abstract import HealthBar
from src.entities.modifiers_and_characteristics import (
    HealthLifeCharacteristics,
    AsteroidLifeCharacteristics,
)


class DefaultHealthBar(HealthBar, ABC):
    border_color = "yellow"

    def __init__(self, pos: Vec2d, w: float, h: float):
        self.pos = pos
        self.w = w
        self.h = h

    def draw_health_line(self, screen: Surface, pos: Vec2d, health: float, color: Union[str, Tuple[int, int, int]]):
        x, y = pos + self.pos
        pygame.draw.rect(
            screen,
            self.__class__.border_color,
            (x - 1, y - 1, self.w + 2, self.h + 2),
            width=3,
        )
        pygame.draw.rect(screen, color, (x, y, self.w * health, self.h))


class BasicHealthBar(DefaultHealthBar, ABC):

    def render(
        self,
        screen: Surface,
        life_characteristics: HealthLifeCharacteristics,
        pos: Vec2d,
    ):
        health = life_characteristics.health_fullness()
        self.draw_health_line(screen, pos, health, color=self.__class__.color)


class AllyBar(BasicHealthBar):
    color = "green"


class NeutralBar(BasicHealthBar):
    color = "yellow"
    border_color = "red"


class EnemyBar(BasicHealthBar):
    color = "red"


class NoHealthBar(HealthBar):
    def render(self, screen: Surface, health: float, pos: Vec2d):
        pass


class AsteroidHealthBar(NeutralBar):

    def render(
        self,
        screen: Surface,
        life_characteristics: AsteroidLifeCharacteristics,
        pos: Vec2d,
    ):
        health = life_characteristics.health_fullness()
        self.draw_health_line(screen, pos, health, color=self.__class__.color)
        mining_health = life_characteristics.mining_health_fullness()
        self.draw_health_line(screen, pos + Vec2d(0, self.h + 6), mining_health, color=(3, 252, 223))
