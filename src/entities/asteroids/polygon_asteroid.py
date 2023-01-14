import math
from dataclasses import dataclass
from typing import Tuple, List, Dict

import pygame
import pymunk
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView
from src.entities.asteroids.abstract import AsteroidViewData, AbstractAsteroidView, AbstractAsteroid
from src.entities.basic_entity.view import PolyBasicView
from src.utils.get_polygon_verts import apply_rotation_for_verts
from src.utils.polygon_area import polygon_area

"""
That works, but too slow.
"""


@dataclass
class PolygonAsteroidViewData(AsteroidViewData):
    polygons: List[List[Tuple[float, float]]]
    vertices: List[Tuple[float, float]]


class PolygonAsteroidView(AbstractAsteroidView, PolyBasicView):

    view_data: PolygonAsteroidViewData

    def draw_image(self, screen: pygame.Surface, pos: Vec2d) -> None:
        verts = apply_rotation_for_verts(
            self.entity.shape.get_vertices(), self.entity.angle, pos
        )
        pygame.draw.polygon(screen, self.view_data.color, verts)
        pygame.draw.polygon(screen, (0, 0, 0), verts, width=2)
        for polygon in self.view_data.polygons:
            verts = apply_rotation_for_verts(polygon, self.entity.angle, pos)
            pygame.draw.polygon(screen, self.view_data.resource_color, verts)


class PolygonAsteroid(AbstractAsteroid):

    view_data: PolygonAsteroidViewData

    def create_moment(self) -> float:
        return pymunk.moment_for_poly(self.create_mass(), self.view_data.vertices)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Poly(None, self.view_data.vertices)

    def create_view(self) -> EntityView:
        return PolygonAsteroidView(self, self.view_data)

    def get_area(self) -> float:
        return polygon_area(self.view_data.vertices)

    @classmethod
    def get_view_data_from_dict(cls, data: Dict) -> PolygonAsteroidViewData:
        return PolygonAsteroidViewData.from_dict(data)
