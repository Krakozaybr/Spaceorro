from abc import abstractmethod, ABC
from typing import Tuple, Union

import pygame
import pymunk
from pymunk import Vec2d

from src.abstract import RenderUpdateObject, Serializable, Updateable
from src.entities.config.abstract_config import AbstractEntityConfig


class Engine:
    rotation_speed: float
    direct_force: float
    max_speed: float
    max_rotation_speed: float
    stop_coef: float
    stop_rotation_coef: float
    body: pymunk.Body
    control_body: pymunk.Body

    @abstractmethod
    def stop(self, dt: float, vertical: bool, horizontal: bool, rotation: bool):
        pass

    @abstractmethod
    def rotate_clockwise(self, dt: float, power: float):
        pass

    @abstractmethod
    def rotate_counterclockwise(self, dt: float, power: float):
        pass

    @abstractmethod
    def rotate_to(self, dt: float, alpha: float):
        pass

    @abstractmethod
    def move_to(self, pos: Vec2d):
        pass

    @abstractmethod
    def apply_force(self, force: Vec2d, dt: float):
        pass

    @abstractmethod
    def bring_rotate_speed_to(self, dt: float, speed: float):
        pass

    @abstractmethod
    def bring_speed_to(self, dt: float, speed: float):
        pass


class HealthBar(ABC):
    pos: Vec2d
    w: float
    h: float
    color: Union[str, Tuple[int, int, int]]

    @abstractmethod
    def render(self, screen, health: float, pos: Vec2d):
        pass


class EntityView(pygame.sprite.Sprite, ABC):
    @abstractmethod
    def draw(self, screen, pos: Vec2d):
        pass


class Entity(Serializable, pymunk.Body, RenderUpdateObject, ABC):

    view: EntityView
    health: float
    max_health: float
    is_active: bool
    is_alive: bool
    shape: pymunk.Shape
    control_body: pymunk.Body
    pivot: pymunk.PivotJoint
    engine: Engine
    health_bar: HealthBar
    config: AbstractEntityConfig

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
