from abc import ABC, abstractmethod
from typing import Dict, Optional

import pymunk
from pygame import Surface
from pymunk import Vec2d

from src.entities.abstract import GuidedEntity, Pilot, EntityView
from src.entities.characteristics import (
    LifeCharacteristics,
    WeaponCharacteristics,
    VelocityCharacteristics,
)
from src.entities.config.abstract_config import AbstractEntityConfig
from src.entities.gadgets.engines.abstract import Engine
from src.settings import get_entity_start_config
from src.utils.body_serialization import *


class BasicEntity(GuidedEntity, ABC):
    CONFIG_NAME: str
    START_CONFIG_NAME: str
    config: AbstractEntityConfig
    engine: Engine

    def __init__(
        self,
        pos: Vec2d,
        life_characteristics: LifeCharacteristics,
        velocity_characteristics: VelocityCharacteristics,
        weapon_characteristics: WeaponCharacteristics,
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
        self.weapon_characteristics = weapon_characteristics
        self.velocity_characteristics = velocity_characteristics
        self.is_active = True

        # Instruments
        self.engine = self.create_engine()
        self.pilot = self.create_pilot()
        self.view = self.create_view()

    @property
    def is_alive(self) -> bool:
        return self.life_characteristics.health > 0

    @abstractmethod
    def create_engine(self) -> Engine:
        pass

    @abstractmethod
    def create_pilot(self) -> Pilot:
        pass

    @abstractmethod
    def create_view(self) -> EntityView:
        pass

    def render(self, screen: Surface, camera):
        self.view.draw(screen, camera.dv + self.position)

    def update(self, dt):
        self.pilot.update(dt)

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
            "velocity_characteristics": VelocityCharacteristics.from_dict(
                data["velocity_characteristics"]
            ),
            "weapon_characteristics": WeaponCharacteristics.from_dict(
                data["weapon_characteristics"]
            ),
        }

    def characteristics_to_dict(self):
        return {
            "life_characteristics": self.life_characteristics.to_dict(),
            "velocity_characteristics": self.velocity_characteristics.to_dict(),
            "weapon_characteristics": self.weapon_characteristics.to_dict(),
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
        return {**characteristics, **body_data}
