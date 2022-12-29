from abc import abstractmethod, ABC

import pygame
import pymunk
from pymunk import Vec2d

from src.abstract import RenderUpdateObject, Updateable
from src.entities.config.abstract_config import AbstractEntityConfig
from src.entities.gadgets.engines.abstract import Engine
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.gadgets.weapon.abstract import Weapon
from .characteristics import *
from pygame import Surface


class EntityView(pygame.sprite.Sprite, ABC):
    health_bar: HealthBar

    @abstractmethod
    def draw(self, screen: Surface, pos: Vec2d):
        pass


class Entity(Serializable, pymunk.Body, RenderUpdateObject, ABC):

    view: EntityView
    shape: pymunk.Shape
    control_body: pymunk.Body
    pivot: pymunk.PivotJoint
    engine: Engine
    config: AbstractEntityConfig
    life_characteristics: LifeCharacteristics
    is_active: bool
    is_alive: bool

    def __init__(self, mass: float, moment: float, body_type: int):
        pymunk.Body.__init__(self, mass, moment, body_type)

    @abstractmethod
    def add_to_space(self, space: pymunk.Space):
        pass

    @abstractmethod
    def remove_from_space(self, space: pymunk.Space):
        pass


class EntityFactory(ABC):
    @abstractmethod
    def create_entity(self) -> Entity:
        pass


class Pilot(Updateable, ABC):
    entity: Entity


class GuidedEntity(Entity, ABC):
    pilot: Pilot
    weapon: Weapon
    weapon_characteristics: WeaponCharacteristics
    velocity_characteristics: VelocityCharacteristics
