import math
from math import cos, pi, sin
from random import randint, choice
from typing import List, Tuple

import pygame.sprite
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityFactory
from src.entities.asteroids.abstract import AbstractAsteroid
from src.entities.asteroids.circle_asteroid import (
    CircleAsteroid,
    CircleAsteroidViewData,
)
from src.entities.asteroids.polygon_asteroid import (
    PolygonAsteroid,
    PolygonAsteroidViewData,
)
from src.resources import ResourceType, Resource
from src.utils.polygon_size import get_polygon_size


class AsteroidFactory(EntityFactory):
    @classmethod
    def create_entity(cls, pos: Vec2d) -> AbstractAsteroid:
        # Polygon asteroids are too complex, so the game will be slower with them
        # return cls.create_polygon_asteroid(pos)
        asteroid = cls.create_circle_asteroid(pos)
        asteroid.control_body.velocity = Vec2d(randint(-200, 200), randint(-200, 200))
        return asteroid

    @classmethod
    def create_circle_asteroid(cls, pos: Vec2d):
        radius = cls.generate_radius()
        resource = cls.generate_resource(radius)
        brightness = cls.generate_brightness()
        circles_count = cls.generate_polygons_count()
        return CircleAsteroid(
            pos=pos,
            resource=resource,
            view_data=CircleAsteroidViewData(
                resource_color=resource.resource_type.get_color(),
                color=(brightness, brightness, brightness),
                radius=radius,
                circles=cls.generate_circles(radius, circles_count),
            ),
        )

    @classmethod
    def create_polygon_asteroid(cls, pos: Vec2d):
        vertices_count = cls.generate_vertices_count()
        radius = cls.generate_radius()
        polygons_count = cls.generate_polygons_count()
        vertices = cls.generate_vertices(
            vertices_count=vertices_count,
            r=radius,
        )
        polygons = cls.generate_polygons_for_polygon_asteroid(
            vertices_count=vertices_count, r=radius, polygons_count=polygons_count
        )
        resource = cls.generate_resource(radius)
        brightness = cls.generate_brightness()
        return PolygonAsteroid(
            pos=pos,
            resource=resource,
            view_data=PolygonAsteroidViewData(
                polygons=polygons,
                vertices=vertices,
                resource_color=resource.resource_type.get_color(),
                color=(brightness, brightness, brightness),
                radius=radius,
            ),
        )

    @staticmethod
    def generate_radius() -> float:
        return randint(*AbstractAsteroid.config.polygon_asteroid_radius_interval)

    @staticmethod
    def generate_vertices_count() -> int:
        return randint(*PolygonAsteroid.config.polygon_asteroid_vertices_count)

    @staticmethod
    def generate_polygons_count() -> int:
        return randint(*PolygonAsteroid.config.polygon_asteroid_polygons_count)

    @staticmethod
    def generate_brightness() -> int:
        return randint(*AbstractAsteroid.config.brightness)

    @staticmethod
    def generate_resource(radius: float) -> Resource:
        resource_type = choice(list(ResourceType))
        resource_quantity = radius * randint(100, 200) / 100
        resource = Resource(quantity=resource_quantity, resource_type=resource_type)
        return resource

    @staticmethod
    def generate_vertices(vertices_count: int, r: float) -> List[Tuple[float, float]]:
        vertices = []
        step = 2 * pi / vertices_count
        for i in range(vertices_count):
            angle = randint(int(step * i * 100), int(step * (i + 1) * 100)) / 100
            vertices.append((r * cos(angle), r * sin(angle)))
        return vertices

    """
    Generates polygons inside asteroid, they will be painted as color of resource.
    So, they are like markers for players
    
    *The solution below should be improved
    """

    @classmethod
    def generate_polygons_for_polygon_asteroid(
            cls, vertices_count: int, r: float, polygons_count: int
    ) -> List[List[Tuple[float, float]]]:
        a = 2 * pi / vertices_count
        polygon_radius = cos(a) * r / 2
        polygons = []
        masks = []
        for _ in range(polygons_count):
            polygon_vertices_count = randint(3, 7)
            vertices = cls.generate_vertices(
                vertices_count=polygon_vertices_count, r=polygon_radius
            )
            max_attempts = 20
            attempts = 0

            new_vertices = cls.generate_translated_polygon(polygon_radius, vertices)
            mask = cls.get_mask_from_polygon(new_vertices)

            while (
                    len(masks)
                    and any(mask.overlap(i, (0, 0)) for i in masks)
                    and attempts < max_attempts
            ):
                new_vertices = cls.generate_translated_polygon(polygon_radius, vertices)
                mask = cls.get_mask_from_polygon(new_vertices)
                attempts += 1

            masks.append(mask)
            polygons.append(vertices)

        return polygons

    @staticmethod
    def generate_circles(radius: float, count: int) -> List[Tuple[Vec2d, float]]:
        result = []

        (
            min_inner_radius,
            max_inner_radius,
        ) = AbstractAsteroid.config.inner_circle_radius_interval
        for _ in range(count):
            inner_radius = randint(min_inner_radius * 100, max_inner_radius * 100) / 100
            result.append(
                (
                    Vec2d(1, 0)
                        .rotated(randint(0, int(math.pi * 200)) / 100)
                        .normalized()
                    * (radius - inner_radius),
                    inner_radius,
                )
            )
        return result

    @staticmethod
    def generate_translated_polygon(
            polygon_radius: float, polygon: List[Tuple[float, float]]
    ):
        dx = randint(0, int(polygon_radius * 100)) / 100
        dy = randint(0, int(polygon_radius * 100)) / 100
        return [(x + dx, y + dy) for x, y in polygon]

    @staticmethod
    def get_mask_from_polygon(polygon: List[Tuple[float, float]]) -> pygame.mask.Mask:
        w, h = get_polygon_size(polygon)
        surface = pygame.Surface((w, h))
        pygame.draw.lines(surface, "red", True, polygon)
        return pygame.mask.from_surface(surface)
