from abc import abstractmethod, ABC
import pygame
import pymunk
from pymunk import Vec2d

from src.abstract import RenderUpdateObject, Serializable


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
    def rotate_clockwise(self, dt: float):
        pass

    @abstractmethod
    def rotate_counterclockwise(self, dt: float):
        pass

    @abstractmethod
    def apply_force(self, force: Vec2d, dt: float):
        pass


class EntityView(pygame.sprite.Sprite, ABC):
    @abstractmethod
    def draw(self, screen, pos):
        pass


class Entity(Serializable, pymunk.Body, RenderUpdateObject, ABC):

    view: EntityView
    health: float
    max_health: float
    is_active: bool
    shape: pymunk.Shape
    control_body: pymunk.Body
    pivot: pymunk.PivotJoint
    engine: Engine

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


class Pilot(RenderUpdateObject, ABC):
    entity: Entity
