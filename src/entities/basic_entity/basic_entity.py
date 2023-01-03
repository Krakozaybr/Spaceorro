from abc import ABC, abstractmethod
from typing import Optional

import pymunk
from pygame import Surface
from pymunk import Vec2d

from src.entities.abstract.abstract import Entity, EntityView, ENTITY_COLLISION
from src.entities.entity_configs import PolyEntityConfig
from src.entities.modifiers_and_characteristics import (
    LifeCharacteristics,
)
from src.utils.body_serialization import *


class BasicEntity(Entity, ABC):
    config_name: str

    def __init__(
        self,
        pos: Vec2d,
        life_characteristics: Optional[LifeCharacteristics] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        entity_id: Optional[int] = None,
    ):
        if entity_id is not None:
            self.id = entity_id

        # Pymunk
        if moment is None:
            moment = self.create_moment()
        if mass is None:
            mass = self.config.mass

        super().__init__(mass, moment, body_type=pymunk.Body.DYNAMIC)

        self.shape = self.create_shape()
        self.shape.collision_type = ENTITY_COLLISION
        self.position = pos

        self.control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.control_body.position = pos

        self.pivot = pymunk.PivotJoint(self.control_body, self, (0, 0), (0, 0))
        self.pivot.max_bias = 0  # disable joint correction

        # Characteristics
        if life_characteristics is None:
            life_characteristics = self.create_life_characteristics()
        self.life_characteristics = life_characteristics

        # Basic
        self.is_active = True
        self.view = self.create_view()

    @abstractmethod
    def create_life_characteristics(self) -> LifeCharacteristics:
        pass

    @abstractmethod
    def create_moment(self) -> float:
        pass

    @abstractmethod
    def create_shape(self) -> pymunk.Shape:
        pass

    @property
    def is_alive(self) -> bool:
        return self.life_characteristics.is_alive()

    @abstractmethod
    def create_view(self) -> EntityView:
        pass

    def render(self, screen: Surface, camera) -> None:
        self.view.draw(screen, camera.dv + self.position)

    def add_to_space(self, space: pymunk.Space) -> None:
        super().add_to_space(space)
        space.add(self, self.shape)
        space.add(self.control_body)
        space.add(self.pivot)

    def remove_from_space(self, space: pymunk.Space) -> None:
        super().remove_from_space(space)
        space.remove(self, self.shape)
        space.remove(self.control_body)
        space.remove(self.pivot)

    @staticmethod
    @abstractmethod
    def get_characteristics(data: Dict) -> Dict:
        pass

    def characteristics_to_dict(self) -> Dict:
        return {
            "life_characteristics": self.life_characteristics.to_dict(),
        }

    def collide(self, other: Entity):
        other.take_damage(self.mass * self.velocity.length / 100)

    def to_dict(self) -> Dict:
        characteristics = self.characteristics_to_dict()
        body_data = {
            "id": self.id,
            "body": dynamic_body_to_dict(self),
            "control_body": kinematic_body_to_dict(self.control_body),
        }
        return {"class_name": self.__class__.__name__, **characteristics, **body_data}

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__) and self.id == other.id:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self.id)


class PolyBasicEntity(BasicEntity, ABC):

    config: PolyEntityConfig

    def create_moment(self) -> float:
        return pymunk.moment_for_poly(self.config.mass, self.config.vertices)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Poly(self, self.config.vertices)
