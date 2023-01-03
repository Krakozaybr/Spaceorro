from abc import ABC, abstractmethod
from math import inf

import pygame
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView, Entity
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.settings import SHOW_VELOCITY_VECTOR, SHOW_PLAYER_COLLISION_POLY


class BasicView(EntityView, ABC):

    # Are inited in init_sizes()
    w: float
    h: float
    left_top_corner_delta: Vec2d

    def __init__(self, entity: Entity, *groups: AbstractGroup):
        super().__init__(*groups)
        self.entity = entity
        self.init_sizes()
        self.health_bar = self.create_health_bar()

    @abstractmethod
    def create_health_bar(self) -> HealthBar:
        pass

    @abstractmethod
    def init_sizes(self):
        pass

    def draw(self, screen: pygame.Surface, pos: Vec2d) -> None:
        if hasattr(self, "image") and self.image is not None:
            x, y = self.left_top_corner_delta + pos
            self.image.blit(screen, (x, y))
        if SHOW_VELOCITY_VECTOR:
            x, y = pos
            dx, dy = x + self.entity.velocity.x / 10, y + self.entity.velocity.y / 10
            pygame.draw.line(screen, "blue", (x, y), (dx, dy))
        self.draw_health_bar(screen, pos)

    @abstractmethod
    def draw_health_bar(self, screen: pygame.Surface, pos: Vec2d):
        pass


class PolyBasicView(BasicView, ABC):
    def draw(self, screen: pygame.Surface, pos: Vec2d) -> None:
        super().draw(screen, pos)
        if SHOW_PLAYER_COLLISION_POLY:
            verts = []
            shape = self.entity.shape
            for v in shape.get_vertices():
                x = v.rotated(shape.body.angle)[0]
                y = v.rotated(shape.body.angle)[1]
                verts.append((x + pos.x, y + pos.y))
            pygame.draw.polygon(screen, "red", [(dx, dy) for dx, dy in verts], width=1)

    def init_sizes(self):
        min_x = min_y = inf
        max_x = max_y = -inf
        for x, y in self.entity.shape.get_vertices():
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)
        self.w = max_x - min_x
        self.h = max_y - min_y
        self.right_top_corner_delta = Vec2d(-self.w / 2, -self.h / 2)
