from abc import ABC, abstractmethod
from typing import Optional

import pymunk
from pygame import Surface
from pymunk import Vec2d

from src.entities.abstract.abstract import Entity, EntityView, ENTITY_COLLISION
from src.entities.entity_configs import PolyEntityConfig, EntityWithFixedMassConfig
from src.entities.modifiers_and_characteristics import (
    LifeCharacteristics,
)
from src.utils.body_serialization import *
from src.utils.signal import Signal, SignalFieldMixin


class BasicEntity(Entity, SignalFieldMixin, ABC):

    on_death = Signal()

    def __init__(
        self,
        pos: Vec2d,
        life_characteristics: Optional[LifeCharacteristics] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        entity_id: Optional[int] = None,
    ):
        SignalFieldMixin.__init__(self)
        # Pymunk
        if mass is None:
            mass = self.create_mass()
        if moment is None:
            moment = self.create_moment()
        Entity.__init__(
            self, mass, moment, body_type=pymunk.Body.DYNAMIC, _obj_id=entity_id
        )

        self.shape = self.create_shape()
        self.shape.collision_type = ENTITY_COLLISION
        self.shape.elasticity = 90

        self.shape.body = self
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
        self.in_space = False
        self.view = self.create_view()

    @abstractmethod
    def create_mass(self) -> float:
        pass

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

    @abstractmethod
    def die(self):
        self.on_death.emit()

    def render(self, screen: Surface, camera) -> None:
        self.view.draw(screen, camera.dv + self.position)

    def add_to_space(self, space: pymunk.Space) -> None:
        if not self.in_space:
            space.add(self, self.shape)
            space.add(self.control_body)
            space.add(self.pivot)
        super().add_to_space(space)

    def remove_from_space(self, space: pymunk.Space) -> None:
        if self.in_space:
            space.remove(self, self.shape)
            space.remove(self.control_body)
            space.remove(self.pivot)
        super().remove_from_space(space)

    @staticmethod
    @abstractmethod
    def get_characteristics(data: Dict) -> Dict:
        pass

    def characteristics_to_dict(self) -> Dict:
        return {
            "life_characteristics": self.life_characteristics.to_dict(),
        }

    def collide(self, other: Entity):
        other.take_damage(
            self.mass * (other.velocity - self.velocity).length / 100000, self
        )

    def apply_params_to_bodies(self, data: Dict):
        apply_params_to_dynamic_body_from_dict(self, data["body"])
        apply_params_to_kinematic_body_from_dict(
            self.control_body, data["control_body"]
        )

    def to_dict(self) -> Dict:
        characteristics = self.characteristics_to_dict()
        body_data = {
            "obj_id": self.obj_id,
            "body": dynamic_body_to_dict(self),
            "control_body": kinematic_body_to_dict(self.control_body),
        }
        return {**super().to_dict(), **characteristics, **body_data}

    @classmethod
    def get_default_params(cls, data: Dict) -> Dict:
        return {
            "entity_id": data["obj_id"],
            "pos": data["body"]["position"],
            "mass": data["body"]["mass"],
            "moment": data["body"]["moment"],
            **cls.get_characteristics(data),
        }

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__) and self.obj_id == other.obj_id:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self.obj_id)


class PolyBasicEntity(BasicEntity, ABC):

    config: PolyEntityConfig

    def create_moment(self) -> float:
        return pymunk.moment_for_poly(self.config.mass, self.config.vertices)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Poly(self, self.config.vertices)


class EntityWithFixedMass(BasicEntity, ABC):
    config: EntityWithFixedMassConfig

    def create_mass(self) -> float:
        return self.config.mass
