from abc import ABCMeta, abstractmethod
from src.utils.vector import Vector
import pygame


class Engine:
    rotation_speed: float
    direct_speed: float


class Pilot:
    pass


class Entity(pygame.sprite.Sprite, metaclass=ABCMeta):
    pos: Vector
    speed: Vector
    acceleration: Vector
    movement_strategy: Engine
    pilot: Pilot
    health: float
    max_health: float

    @abstractmethod
    def render(self, screen, dt: int):
        pass

    @abstractmethod
    def update(self, dt):
        pass
