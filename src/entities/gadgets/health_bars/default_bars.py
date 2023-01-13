from abc import ABC
from typing import Tuple, Union, Optional

import pygame.draw
from pygame import Surface
from pymunk import Vec2d

from src.entities.abstract.abstract import HealthBar
from src.entities.modifiers_and_characteristics import (
    HealthLifeCharacteristics,
    AsteroidLifeCharacteristics,
)
from src.settings import HEALTH_BAR_H, HEALTH_BAR_FONT_SIZE, HEALTH_BAR_FONT_COLOR


class DefaultHealthBar(HealthBar, ABC):
    border_color = "red"

    def __init__(self, pos: Vec2d, w: float):
        self.pos = pos
        self.w = w
        self.h = HEALTH_BAR_H
        self.font = pygame.font.Font(None, HEALTH_BAR_FONT_SIZE)

    def draw_health_line(
        self,
        screen: Surface,
        pos: Vec2d,
        health: float,
        max_health: float,
        color: Union[str, Tuple[int, int, int]],
    ):
        x, y = pos + self.pos
        pygame.draw.rect(
            screen,
            self.__class__.border_color,
            (x - 1, y - 1, self.w + 2, self.h + 2),
        )
        pygame.draw.rect(screen, color, (x, y, self.w * health / max_health, self.h))
        health_text = self.font.render(
            f"{round(health)}/{round(max_health)}", False, HEALTH_BAR_FONT_COLOR
        )
        screen.blit(
            health_text,
            (
                x + self.w / 2 - health_text.get_width() / 2,
                y + (self.h - health_text.get_height()) / 2,
            ),
        )


class BasicHealthBar(DefaultHealthBar, ABC):
    def render(
        self,
        screen: Surface,
        life_characteristics: HealthLifeCharacteristics,
        pos: Vec2d,
    ):
        self.draw_health_line(
            screen,
            pos,
            life_characteristics.health,
            life_characteristics.max_health,
            color=self.__class__.color,
        )


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
    border_color = "blue"

    def render(
        self,
        screen: Surface,
        life_characteristics: AsteroidLifeCharacteristics,
        pos: Vec2d,
    ):
        self.draw_health_line(
            screen,
            pos,
            life_characteristics.health,
            life_characteristics.max_health,
            color=self.__class__.color,
        )
        self.draw_health_line(
            screen,
            pos + Vec2d(0, self.h + 6),
            life_characteristics.mining_health,
            life_characteristics.max_mining_health,
            color=(3, 252, 223),
        )
