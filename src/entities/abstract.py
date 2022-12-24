from abc import ABCMeta, abstractmethod
from src.utils.vector import Vector
import pygame
import pymunk


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


class Entity(metaclass=ABCMeta):
    pos: Vector
    body: pymunk.Body
    shape: pymunk.Shape
    engine: Engine
    view: EntityView
    health: float
    max_health: float

    @abstractmethod
    def render(self, screen, camera):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    # TODO serialization
    # @abstractmethod
    # def serialize(self):
    #     pass
    #
    # @abstractmethod
    # def deserialize(self, data: str):
    #     pass


class EntityFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_entity(self) -> Entity:
        pass


class Pilot:
    entity: Entity

    @abstractmethod
    def render(self, screen, camera):
        pass

    @abstractmethod
    def update(self, dt):
        pass
