from abc import abstractmethod, ABC

import pygame
import pymunk
from pygame import Surface
from pymunk import Vec2d

from src.abstract import RenderUpdateObject, Updateable, Serializable
from src.entities.entity_configs import AbstractEntityConfig
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.modifiers_and_characteristics import *
from src.entities.teams import Team


entities = dict()
current_id = 0
ENTITY_COLLISION = 1


class EntityView(pygame.sprite.Sprite, ABC):
    health_bar: HealthBar

    @abstractmethod
    def draw(self, screen: Surface, pos: Vec2d) -> None:
        pass


class Entity(Serializable, pymunk.Body, RenderUpdateObject, ABC):

    _id: int
    view: EntityView
    shape: pymunk.Shape
    control_body: pymunk.Body
    pivot: pymunk.PivotJoint
    life_characteristics: LifeCharacteristics
    config: AbstractEntityConfig
    __is_active: bool
    is_alive: bool
    in_space: bool

    def __init__(self, mass: float, moment: float, body_type: int):
        pymunk.Body.__init__(self, mass, moment, body_type)
        self.__is_active = False

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @is_active.setter
    def is_active(self, val: bool) -> None:
        self.__is_active = val
        if not self.is_active:
            entities.pop(self.id, None)
        else:
            entities[self.id] = self

    @property
    def id(self) -> int:
        if not hasattr(self, "_id"):
            global current_id
            self._id = current_id
            current_id += 1
        return self._id

    @id.setter
    def id(self, val: int):
        global current_id
        if val >= current_id:
            current_id = val + 1
        self._id = val

    @abstractmethod
    def add_to_space(self, space: pymunk.Space) -> None:
        self.in_space = True

    @abstractmethod
    def remove_from_space(self, space: pymunk.Space) -> None:
        self.in_space = False

    @abstractmethod
    def take_damage(self, damage: float) -> None:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    @abstractmethod
    def collide(self, other):
        pass


class EntityFactory(ABC):
    @abstractmethod
    def create_entity(self) -> Entity:
        pass


class Pilot(Updateable, ABC):
    entity: Entity
    team: Team
