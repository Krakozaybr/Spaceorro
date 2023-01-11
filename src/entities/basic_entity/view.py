from abc import ABC, abstractmethod
from math import inf

import pygame
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView, Entity
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.settings import SHOW_VELOCITY_VECTOR, SHOW_PLAYER_COLLISION_POLY
from src.utils.get_polygon_verts import apply_rotation_for_verts
from src.utils.polygon_size import get_polygon_size


class BasicView(EntityView, ABC):

    # Are inited in init_sizes()
    w: float
    h: float
    right_top_corner_delta: Vec2d

    def __init__(self, entity: Entity, *groups: AbstractGroup):
        super().__init__(*groups)
        self.entity = entity
        self.init_sizes()

    @abstractmethod
    def init_sizes(self):
        pass

    def draw_image(self, screen: pygame.Surface, pos: Vec2d) -> None:
        if hasattr(self, "image") and self.image is not None:
            x, y = pos
            screen.blit(
                self.image,
                (x - self.image.get_width() / 2, y - self.image.get_height() / 2),
            )

    def draw(self, screen: pygame.Surface, pos: Vec2d) -> None:
        self.draw_image(screen, pos)
        if SHOW_VELOCITY_VECTOR:
            x, y = pos
            dx, dy = x + self.entity.velocity.x / 10, y + self.entity.velocity.y / 10
            pygame.draw.line(screen, "blue", (x, y), (dx, dy))


class PolyBasicView(BasicView, ABC):
    def draw(self, screen: pygame.Surface, pos: Vec2d) -> None:
        super().draw(screen, pos)
        if SHOW_PLAYER_COLLISION_POLY:
            verts = apply_rotation_for_verts(
                self.entity.shape.get_vertices(), self.entity.angle, pos
            )
            pygame.draw.polygon(screen, "red", [(dx, dy) for dx, dy in verts], width=1)

    def init_sizes(self):
        self.w, self.h = get_polygon_size(self.entity.shape.get_vertices())
        self.right_top_corner_delta = Vec2d(-self.w / 2, -self.h / 2)


class HealthBarMixin(BasicView, ABC):
    health_bar: HealthBar

    def __init__(self, entity: Entity, *groups: AbstractGroup):
        BasicView.__init__(self, entity, *groups)
        self.health_bar = self.create_health_bar()

    @abstractmethod
    def create_health_bar(self) -> HealthBar:
        pass

    def draw(self, screen: pygame.Surface, pos: Vec2d) -> None:
        super().draw(screen, pos)
        self.draw_health_bar(screen, pos)

    @abstractmethod
    def draw_health_bar(self, screen: pygame.Surface, pos: Vec2d):
        pass
