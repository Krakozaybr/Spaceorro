from abc import ABCMeta, abstractmethod
from src.utils.vector import Vector
import pygame
import pymunk
from src.abstract import RenderUpdateObject, Serializable


class Engine:
    rotation_speed: float
    direct_speed: float

    @property
    @abstractmethod
    def current_force(self):
        pass


class EntityView(pygame.sprite.Sprite, metaclass=ABCMeta):

    @abstractmethod
    def draw(self, screen, pos):
        pass


class Entity(Serializable, RenderUpdateObject, metaclass=ABCMeta):
    pos: Vector
    body: pymunk.Body
    shape: pymunk.Shape
    engine: Engine
    view: EntityView
    health: float
    max_health: float


class EntityFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_entity(self) -> Entity:
        pass


class Pilot(RenderUpdateObject):
    entity: Entity
