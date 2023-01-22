from abc import ABC
from typing import Optional, Dict

from pymunk import Vec2d

from src.entities.basic_entity.basic_spaceship import BasicSpaceship
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.modifiers_and_characteristics import (
    WeaponModifiers,
    VelocityCharacteristics,
    HealthLifeCharacteristics,
)
from src.entities.pilots.abstract import Pilot
from src.entities.upgrade_system import SpaceshipUpgradeSystem


class UpgradeableSpaceshipMixin(BasicSpaceship, ABC):

    upgrade_system: SpaceshipUpgradeSystem

    def __init__(
        self,
        pos: Vec2d,
        weapon_modifiers: Optional[WeaponModifiers] = None,
        velocity_characteristics: Optional[VelocityCharacteristics] = None,
        life_characteristics: Optional[HealthLifeCharacteristics] = None,
        upgrade_system: Optional[SpaceshipUpgradeSystem] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        weapon: Optional[AbstractStateWeapon] = None,
        entity_id: Optional[int] = None,
        pilot: Optional[Pilot] = None,
    ):
        super().__init__(
            pos=pos,
            weapon_modifiers=weapon_modifiers,
            velocity_characteristics=velocity_characteristics,
            life_characteristics=life_characteristics,
            mass=mass,
            moment=moment,
            weapon=weapon,
            entity_id=entity_id,
            pilot=pilot,
        )
        if upgrade_system is None:
            upgrade_system = self.create_upgrade_system()
        self.upgrade_system = upgrade_system

    def create_upgrade_system(self) -> SpaceshipUpgradeSystem:
        return SpaceshipUpgradeSystem(self.obj_id)

    def to_dict(self) -> Dict:
        return {**super().to_dict(), "upgrade_system": self.upgrade_system.to_dict()}

    @classmethod
    def get_default_params(cls, data: Dict) -> Dict:
        return {
            **super().get_default_params(data),
            "upgrade_system": SpaceshipUpgradeSystem.from_dict(data["upgrade_system"]),
        }
