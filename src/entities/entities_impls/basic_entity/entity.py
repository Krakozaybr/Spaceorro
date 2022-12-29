from abc import ABC, abstractmethod
from typing import Dict

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
    ):
        # Pymunk
        moment = pymunk.moment_for_poly(self.config.MASS, self.config.VERTICES)
        super().__init__(self.config.MASS, moment, body_type=pymunk.Body.DYNAMIC)

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
        self.is_alive = True

        # Instruments
        self.engine = self.create_engine()
        self.pilot = self.create_pilot()
        self.view = self.create_view()

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
            "life_characteristics": LifeCharacteristics.deserialize(
                data["life_characteristics"]
            ),
            "velocity_characteristics": VelocityCharacteristics.deserialize(
                data["velocity_characteristics"]
            ),
            "weapon_characteristics": WeaponCharacteristics.deserialize(
                data["weapon_characteristics"]
            ),
        }

    def serialize_characteristics(self):
        return {
            "life_characteristics": self.life_characteristics.serialize(),
            "velocity_characteristics": self.velocity_characteristics.serialize(),
            "weapon_characteristics": self.weapon_characteristics.serialize(),
        }

    @classmethod
    def create_default(cls, pos=Vec2d.zero()):
        data = get_entity_start_config(cls.START_CONFIG_NAME)
        print(cls.get_characteristics(data))
        return cls(pos=pos, **cls.get_characteristics(data))
