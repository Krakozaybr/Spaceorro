from abc import ABC, abstractmethod
from typing import Optional

from pymunk import Vec2d

from src.entities.abstract import GuidedEntity, Pilot
from src.entities.characteristics import (
    LifeCharacteristics,
    WeaponCharacteristics,
    VelocityCharacteristics,
)
from src.entities.entities_impls.basic_entity.basic_entity import BasicEntity
from src.entities.gadgets.engines.abstract import Engine
from src.utils.body_serialization import *


class BasicGuidedEntity(GuidedEntity, BasicEntity, ABC):
    def __init__(
        self,
        pos: Vec2d,
        life_characteristics: LifeCharacteristics,
        velocity_characteristics: VelocityCharacteristics,
        weapon_characteristics: WeaponCharacteristics,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
    ):
        BasicEntity.__init__(
            self,
            pos=pos,
            life_characteristics=life_characteristics,
            mass=mass,
            moment=moment,
        )

        # Characteristics
        self.weapon_characteristics = weapon_characteristics
        self.velocity_characteristics = velocity_characteristics

        # Instruments
        self.engine = self.create_engine()
        self.pilot = self.create_pilot()

    @property
    def is_alive(self) -> bool:
        return self.life_characteristics.health > 0

    @abstractmethod
    def create_engine(self) -> Engine:
        pass

    @abstractmethod
    def create_pilot(self) -> Pilot:
        pass

    def update(self, dt):
        self.pilot.update(dt)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            "velocity_characteristics": VelocityCharacteristics.from_dict(
                data["velocity_characteristics"]
            ),
            "weapon_characteristics": WeaponCharacteristics.from_dict(
                data["weapon_characteristics"]
            ),
            **super().get_characteristics(data),
        }

    def characteristics_to_dict(self):
        return {
            "velocity_characteristics": self.velocity_characteristics.to_dict(),
            "weapon_characteristics": self.weapon_characteristics.to_dict(),
            **super().characteristics_to_dict(),
        }
