from abc import ABC
from typing import Dict

import pymunk

from src.entities.basic_entity.basic_entity import BasicEntity
from src.entities.entity_configs import PickupableEntityConfig
from src.entities.modifiers_and_characteristics import (
    LifeCharacteristics,
    TemporaryObjectLifeCharacteristics,
)
from src.settings import get_pickupable_config


class Pickupable(BasicEntity, ABC):

    life_characteristics: TemporaryObjectLifeCharacteristics
    config: PickupableEntityConfig
    config_name: str

    def create_life_characteristics(self) -> LifeCharacteristics:
        return TemporaryObjectLifeCharacteristics.from_dict(
            get_pickupable_config(self.config_name)
        )

    def create_moment(self) -> float:
        return pymunk.moment_for_circle(self.create_mass(), 0, self.config.radius)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Circle(None, self.config.radius)

    def die(self):
        self.life_characteristics.decrease(self.life_characteristics.life_time)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return dict()

    def update(self, dt: float):
        self.life_characteristics.decrease(dt)
        if not self.is_alive:
            self.is_active = False
