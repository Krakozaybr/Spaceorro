from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List, Union

import pygame
import pymunk
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView, Entity, SaveStrategy
from src.entities.basic_entity.basic_entity import BasicEntity
from src.entities.basic_entity.view import PolyBasicView, HealthBarMixin
from src.entities.entity_configs import AsteroidEntityConfig
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.gadgets.health_bars.default_bars import AsteroidHealthBar
from src.entities.modifiers_and_characteristics import (
    AsteroidLifeCharacteristics,
)
from src.entities.pickupable.resource import PickupableResource
from src.environment.abstract import get_environment
from src.resources import Resource
from src.settings import get_asteroid_config, DUST_PARTICLE_IMAGE, load_image
from src.utils.get_polygon_verts import apply_rotation_for_verts
from src.utils.serializable_dataclass import SerializableDataclass


@dataclass
class ViewData(SerializableDataclass):
    polygons: List[List[Tuple[float, float]]]
    vertices: List[Tuple[float, float]]
    resource_color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]


class AsteroidView(PolyBasicView, HealthBarMixin):

    dust_image = load_image(DUST_PARTICLE_IMAGE)
    view_data: ViewData

    def __init__(self, entity: Entity, view_data: ViewData, *groups: AbstractGroup):
        super().__init__(entity, *groups)
        self.view_data = view_data

    def draw_image(self, screen: pygame.Surface, pos: Vec2d) -> None:
        verts = apply_rotation_for_verts(
            self.entity.shape.get_vertices(), self.entity.angle, pos
        )
        pygame.draw.polygon(screen, self.view_data.color, verts)
        pygame.draw.polygon(screen, (0, 0, 0), verts, width=2)
        for polygon in self.view_data.polygons:
            verts = apply_rotation_for_verts(polygon, self.entity.angle, pos)
            pygame.draw.polygon(screen, self.view_data.resource_color, verts)

    def create_health_bar(self) -> HealthBar:
        return AsteroidHealthBar(Vec2d(-self.w / 2 - 2, -self.h + 4), self.w + 4, 8)

    def draw_health_bar(self, screen: pygame.Surface, pos: Vec2d):
        self.health_bar.render(
            screen,
            self.entity.life_characteristics,
            pos,
        )


class Asteroid(BasicEntity):

    resource: Resource
    life_characteristics: AsteroidLifeCharacteristics
    view_data: ViewData
    config = AsteroidEntityConfig.from_dict(get_asteroid_config())
    save_strategy = SaveStrategy.ENTITY

    def __init__(
        self,
        pos: Vec2d,
        resource: Resource,
        view_data: ViewData,
        life_characteristics: Optional[AsteroidLifeCharacteristics] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        entity_id: Optional[int] = None,
    ):
        self.view_data = view_data
        self.resource = resource
        self.resource_launched = False
        super().__init__(
            pos=pos,
            life_characteristics=life_characteristics,
            mass=mass,
            moment=moment,
            entity_id=entity_id,
        )

    def create_mass(self) -> float:
        return self.shape.area * self.config.mass_coef

    def create_life_characteristics(self) -> AsteroidLifeCharacteristics:
        health = self.shape.area * self.config.health_area_coef
        mining_health = self.shape.area * self.config.mining_health_area_coef
        return AsteroidLifeCharacteristics(
            health=health,
            max_health=health,
            mining_health=mining_health,
            max_mining_health=mining_health,
        )

    def create_moment(self) -> float:
        return pymunk.moment_for_poly(self.create_mass(), self.view_data.vertices)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Poly(None, self.view_data.vertices)

    def create_view(self) -> EntityView:
        return AsteroidView(self, self.view_data)

    def die(self):
        self.life_characteristics.decrease(self.life_characteristics.health)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            "life_characteristics": AsteroidLifeCharacteristics.from_dict(
                data["life_characteristics"]
            )
        }

    def take_damage(self, damage: float) -> None:
        self.life_characteristics.decrease(damage)

    def mine(self, damage: float):
        self.life_characteristics.decrease_by_mining(damage)

    def to_dict(self) -> Dict:
        return {
            **super().to_dict(),
            "resource": self.resource.to_dict(),
            "view_data": self.view_data.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        res = cls(
            resource=Resource.from_dict(data["resource"]),
            view_data=ViewData.from_dict(data["view_data"]),
            **cls.get_default_params(data)
        )
        cls.apply_params_to_bodies(res, data)
        return res

    def launch_resource(self, losses_coef):
        registrator = get_environment().get_entity_registrator()
        registrator.add_entity(
            PickupableResource(pos=self.position, resource=self.resource * losses_coef)
        )
        self.resource_launched = True
        self.is_active = False
        self.save_strategy = SaveStrategy.NOT_SAVE

    def update(self, dt: float):
        if not self.is_alive and not self.resource_launched:
            if self.life_characteristics.is_mined():
                self.launch_resource(1)
            elif self.life_characteristics.is_destroyed():
                self.launch_resource(self.config.losses_coef)
