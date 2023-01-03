from abc import ABC

import pygame.draw
from pygame import Surface
from pymunk import Vec2d

from src.entities.abstract.abstract import HealthBar


class DefaultBar(HealthBar, ABC):
    border_color = "yellow"

    def __init__(self, pos: Vec2d, w: float, h: float):
        self.pos = pos
        self.w = w
        self.h = h

    def render(self, screen: Surface, health: float, pos: Vec2d):
        x, y = pos + self.pos
        pygame.draw.rect(
            screen,
            self.__class__.border_color,
            (x - 1, y - 1, self.w + 2, self.h + 2),
            width=3,
        )
        pygame.draw.rect(screen, self.__class__.color, (x, y, self.w * health, self.h))


class AllyBar(DefaultBar):
    color = "green"


class NeutralBar(DefaultBar):
    color = "yellow"
    border_color = "red"


class EnemyBar(DefaultBar):
    color = "red"


class NoHealthBar(HealthBar):
    def render(self, screen: Surface, health: float, pos: Vec2d):
        pass
