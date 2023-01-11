from math import cos, pi, sin
from random import randint, choice
from typing import List, Tuple

import pygame.sprite
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityFactory
from src.entities.asteroids.asteroid import Asteroid, ViewData
from src.resources import ResourceType, Resource
from src.utils.polygon_size import get_polygon_size


class AsteroidFactory(EntityFactory):
    @classmethod
    def create_entity(cls, pos: Vec2d) -> Asteroid:
        vertices_count = randint(*Asteroid.config.vertices_count)
        radius = randint(*Asteroid.config.radius_interval)
        polygons_count = randint(*Asteroid.config.polygons_count)
        vertices = cls.generate_vertices(
            vertices_count=vertices_count,
            r=radius,
        )
        polygons = cls.generate_polygons(
            vertices_count=vertices_count, r=radius, polygons_count=polygons_count
        )
        resource_type = choice(list(ResourceType))
        resource_quantity = radius * randint(100, 200) / 100
        resource = Resource(quantity=resource_quantity, resource_type=resource_type)
        brightness = randint(40, 255)

        return Asteroid(pos=pos, resource=resource, view_data=ViewData(
            polygons=polygons,
            vertices=vertices,
            resource_color=ResourceType.get_color(resource_type),
            color=(brightness, brightness, brightness)
        ))

    @staticmethod
    def generate_vertices(vertices_count: int, r: float) -> List[Tuple[float, float]]:
        vertices = []
        step = 2 * pi / vertices_count
        for i in range(vertices_count):
            angle = randint(int(step * i * 100), int(step * (i + 1) * 100)) / 100
            vertices.append((r * cos(angle), r * sin(angle)))
        return vertices

    @classmethod
    def generate_polygons(
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
