from abc import ABC, abstractmethod
from typing import Optional

import pymunk
from pygame import Surface
from pymunk import Vec2d

from src.entities.abstract import Entity, EntityView
from src.entities.characteristics import (
    LifeCharacteristics,
)
from src.settings import get_entity_start_config
from src.utils.body_serialization import *


class BasicEntity(Entity, ABC):
    CONFIG_NAME: str
    START_CONFIG_NAME: str

    def __init__(
        self,
        pos: Vec2d,
        life_characteristics: LifeCharacteristics,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
    ):
        # Pymunk
        if moment is None:
            moment = pymunk.moment_for_poly(self.config.MASS, self.config.VERTICES)
        if mass is None:
            mass = self.config.MASS
        super().__init__(mass, moment, body_type=pymunk.Body.DYNAMIC)

        self.position = pos
        self.shape = pymunk.Poly(self, self.config.VERTICES)

        self.control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.control_body.position = pos

        self.pivot = pymunk.PivotJoint(self.control_body, self, (0, 0), (0, 0))
        self.pivot.max_bias = 0  # disable joint correction

        # Characteristics
        self.life_characteristics = life_characteristics

        # Basic
        self.is_active = True
        self.view = self.create_view()

    @property
    def is_alive(self) -> bool:
        return self.life_characteristics.health > 0

    @abstractmethod
    def create_view(self) -> EntityView:
        pass

    def render(self, screen: Surface, camera):
        self.view.draw(screen, camera.dv + self.position)

    def add_to_space(self, space: pymunk.Space):
        space.add(self, self.shape)
        space.add(self.control_body)
        space.add(self.pivot)

    def remove_from_space(self, space: pymunk.Space):
        space.remove(self, self.shape)
        space.remove(self.control_body)
        space.remove(self.pivot)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            "life_characteristics": LifeCharacteristics.from_dict(
                data["life_characteristics"]
            ),
        }

    def characteristics_to_dict(self):
        return {
            "life_characteristics": self.life_characteristics.to_dict(),
        }

    @classmethod
    def create_default(cls, pos=Vec2d.zero()):
        data = get_entity_start_config(cls.START_CONFIG_NAME)
        return cls(pos=pos, **cls.get_characteristics(data))

    def to_dict(self) -> Dict:
        characteristics = self.characteristics_to_dict()
        body_data = {
            "body": dynamic_body_to_dict(self),
            "control_body": kinematic_body_to_dict(self.control_body),
        }
        return {"class_name": self.__class__.__name__, **characteristics, **body_data}

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.to_dict() == other.to_dict():
            return True
        return False

    def __hash__(self):
        return hash(self.serialize())
