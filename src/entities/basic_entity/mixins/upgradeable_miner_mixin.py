from abc import ABC
from typing import Optional

from pymunk import Vec2d

from src.entities.basic_entity.mixins.upgradeable_spaceship_mixin import (
    UpgradeableSpaceshipMixin,
)
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.modifiers_and_characteristics import (
    MiningCharacteristics,
    VelocityCharacteristics,
    HealthLifeCharacteristics,
    WeaponModifiers,
)
from src.entities.pilots.abstract import Pilot
from src.entities.spaceships.miner.miner_mixin import MinerMixin
from src.entities.upgrade_system import MinerUpgradeSystem


class UpgradeableMinerMixin(MinerMixin, UpgradeableSpaceshipMixin, ABC):

    upgrade_system: MinerUpgradeSystem

    def __init__(
        self,
        pos: Vec2d,
        weapon_modifiers: Optional[WeaponModifiers] = None,
        velocity_characteristics: Optional[VelocityCharacteristics] = None,
        life_characteristics: Optional[HealthLifeCharacteristics] = None,
        mining_characteristics: Optional[MiningCharacteristics] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        weapon: Optional[AbstractStateWeapon] = None,
        entity_id: Optional[int] = None,
        pilot: Optional[Pilot] = None,
        upgrade_system: Optional[MinerUpgradeSystem] = None,
    ):
        MinerMixin.__init__(
            self,
            pos=pos,
            weapon_modifiers=weapon_modifiers,
            velocity_characteristics=velocity_characteristics,
            life_characteristics=life_characteristics,
            mining_characteristics=mining_characteristics,
            mass=mass,
            moment=moment,
            weapon=weapon,
            entity_id=entity_id,
            pilot=pilot,
        )
        UpgradeableSpaceshipMixin.__init__(
            self,
            pos=pos,
            weapon_modifiers=weapon_modifiers,
            velocity_characteristics=velocity_characteristics,
            life_characteristics=life_characteristics,
            upgrade_system=upgrade_system,
            mass=mass,
            moment=moment,
            weapon=weapon,
            entity_id=entity_id,
            pilot=pilot,
        )

    def create_upgrade_system(self) -> MinerUpgradeSystem:
        return MinerUpgradeSystem(self.id)
