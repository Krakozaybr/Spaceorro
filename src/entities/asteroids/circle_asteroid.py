import math
from dataclasses import dataclass
from typing import Tuple, List, Dict

import pygame
import pymunk
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView
from src.entities.asteroids.abstract import (
    AbstractAsteroidView,
    AbstractAsteroid,
    AsteroidViewData,
)


@dataclass
class CircleAsteroidViewData(AsteroidViewData):
    circles: List[Tuple[Vec2d, float]]


class CircleAsteroidView(AbstractAsteroidView):

    view_data: CircleAsteroidViewData

    def init_sizes(self):
        self.w = self.h = self.view_data.radius * 2
        self.right_top_corner_delta = Vec2d(-self.w / 2, -self.h / 2)

    def draw_image(self, screen: pygame.Surface, pos: Vec2d) -> None:
        pygame.draw.circle(screen, self.view_data.color, pos, self.view_data.radius)
        for cir_pos, r in self.view_data.circles:
            pygame.draw.circle(screen, self.view_data.resource_color, cir_pos + pos, r)


class CircleAsteroid(AbstractAsteroid):

    view_data: CircleAsteroidViewData

    def create_moment(self) -> float:
        return pymunk.moment_for_circle(self.create_mass(), 0, self.view_data.radius)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Circle(self, self.view_data.radius)

    def get_area(self) -> float:
        return math.pi * self.view_data.radius ** 2

    def create_view(self) -> EntityView:
        return CircleAsteroidView(self, self.view_data)

    @classmethod
    def get_view_data_from_dict(cls, data: Dict) -> CircleAsteroidViewData:
        return CircleAsteroidViewData.from_dict(data)
