from abc import ABC
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, Optional

from src.abstract import Serializable
from src.entities.basic_entity.basic_spaceship import (
    BasicSpaceshipMixin,
    SpaceshipMixin,
)
from src.entities.modifiers_and_characteristics import (
    HealthLifeCharacteristics,
    WeaponModifiers,
    VelocityCharacteristics,
    MiningCharacteristics,
)
from src.entities.spaceships.miner.miner_mixin import MinerMixin
from src.resources import Resources
from src.settings import get_spaceship_upgrade_config
from src.utils.serializable_dataclass import SerializableDataclass
from src.utils.signal import SignalFieldMixin, Signal
from src.utils.static_init import StaticInitMixin


# Upgrade configs
@dataclass
class UpgradesConfig(SerializableDataclass, ABC):
    start_resources: Resources
    resources_step: Resources


@dataclass
class HealthLifeCharacteristicsUpgradeConfig(UpgradesConfig):
    health_coef_step: float
    armor_step: float


@dataclass
class WeaponModifiersUpgradeConfig(UpgradesConfig):
    bullet_damage_coef_step: float
    bullet_life_time_coef_step: float
    bullet_mass_coef_step: float
    bullet_speed_coef_step: float


@dataclass
class VelocityCharacteristicsUpgradeConfig(UpgradesConfig):
    rotation_speed_coef_step: float
    speed_coef_step: float


@dataclass
class MiningCharacteristicsUpgradeConfig(UpgradesConfig):
    max_level: int


# Upgrades
@dataclass
class Upgrades(SerializableDataclass, StaticInitMixin, SignalFieldMixin, ABC):
    level: int
    config = UpgradesConfig(
        Resources(), Resources()
    )  # dataclasses do not support class fields annotations :(
    changed = Signal()

    def __post_init__(self):
        SignalFieldMixin.__init__(self)
        self.changed.connect(self.level_up)

    def level_up(self):
        self.level += 1

    @property
    def cost(self) -> Resources:
        return self.config.start_resources + self.config.resources_step * self.level

    @property
    def prev_cost(self) -> Resources:
        return self.config.start_resources + self.config.resources_step * (self.level - 1)


@dataclass
class HealthLifeCharacteristicsUpgrades(Upgrades):
    health_upgrade_level: float
    armor_upgrade_level: float

    @classmethod
    def static_init(cls):
        cls.config = HealthLifeCharacteristicsUpgradeConfig.from_dict(
            get_spaceship_upgrade_config("life_characteristics")
        )

    def upgrade_health_coef(self):
        self.health_upgrade_level += 1
        self.changed.emit()

    def upgrade_armor_coef(self):
        self.armor_upgrade_level += 1
        self.changed.emit()

    def apply_upgrades(
        self, standard: HealthLifeCharacteristics, target: HealthLifeCharacteristics
    ):
        target.health = target.health + standard.health * self.config.health_coef_step
        target.max_health = standard.max_health * (
            1 + self.health_upgrade_level * self.config.health_coef_step
        )
        target.armor = (
            standard.armor + self.armor_upgrade_level * self.config.armor_step
        )


@dataclass
class WeaponModifiersUpgrades(Upgrades):
    bullet_damage_upgrade_level: float
    bullet_life_time_upgrade_level: float
    bullet_mass_upgrade_level: float
    bullet_speed_upgrade_level: float

    @classmethod
    def static_init(cls):
        cls.config = WeaponModifiersUpgradeConfig.from_dict(
            get_spaceship_upgrade_config("weapon_modifiers")
        )

    def upgrade_bullet_damage_coef(self):
        self.bullet_damage_upgrade_level += 1
        self.changed.emit()

    def upgrade_bullet_life_time_coef(self):
        self.bullet_life_time_upgrade_level += 1
        self.changed.emit()

    def upgrade_bullet_mass_coef(self):
        self.bullet_mass_upgrade_level += 1
        self.changed.emit()

    def upgrade_bullet_speed_coef(self):
        self.bullet_speed_upgrade_level += 1
        self.changed.emit()

    def apply_upgrades(self, standard: WeaponModifiers, target: WeaponModifiers):
        target.bullet_damage_coef = (
            standard.bullet_damage_coef
            + self.bullet_damage_upgrade_level * self.config.bullet_damage_coef_step
        )
        target.bullet_life_time_coef = (
            standard.bullet_life_time_coef
            + self.bullet_life_time_upgrade_level
            * self.config.bullet_life_time_coef_step
        )
        target.bullet_mass_coef = (
            standard.bullet_mass_coef
            + self.bullet_mass_upgrade_level * self.config.bullet_mass_coef_step
        )
        target.bullet_speed_coef = (
            standard.bullet_speed_coef
            + self.bullet_speed_upgrade_level * self.config.bullet_speed_coef_step
        )


@dataclass
class VelocityCharacteristicsUpgrades(Upgrades):
    rotation_speed_upgrade_level: float
    speed_upgrade_level: float

    @classmethod
    def static_init(cls):
        cls.config = VelocityCharacteristicsUpgradeConfig.from_dict(
            get_spaceship_upgrade_config("velocity_characteristics")
        )

    def upgrade_rotation_speed(self):
        self.rotation_speed_upgrade_level += 1
        self.changed.emit()

    def upgrade_speed(self):
        self.speed_upgrade_level += 1
        self.changed.emit()

    def apply_upgrades(
        self, standard: VelocityCharacteristics, target: VelocityCharacteristics
    ):
        speed_coef = 1 + self.speed_upgrade_level * self.config.speed_coef_step
        rotation_speed_coef = (
            1 + self.rotation_speed_upgrade_level * self.config.rotation_speed_coef_step
        )
        target.direct_force = standard.direct_force * speed_coef
        target.max_speed = standard.max_speed * speed_coef
        target.rotation_speed = standard.rotation_speed * rotation_speed_coef
        target.max_rotation_speed = standard.max_rotation_speed * rotation_speed_coef


class MiningCharacteristicsUpgrades(Upgrades):
    @classmethod
    def static_init(cls):
        cls.config = MiningCharacteristicsUpgradeConfig.from_dict(
            get_spaceship_upgrade_config("mining_upgrades")
        )

    def upgrade_level(self):
        self.changed.emit()

    def can_upgrade(self) -> bool:
        return self.level < self.config.max_level

    def apply_upgrades(
        self, standard: MiningCharacteristics, target: MiningCharacteristics
    ):
        target.level = self.level


# Upgrade System
class SpaceshipUpgradeSystem(Serializable, BasicSpaceshipMixin):
    life_characteristics_upgrades: HealthLifeCharacteristicsUpgrades
    velocity_characteristics_upgrades: VelocityCharacteristicsUpgrades
    weapon_modifiers_upgrades: WeaponModifiersUpgrades

    def __init__(
        self,
        spaceship_id: int,
        life_characteristics_upgrades: Optional[
            HealthLifeCharacteristicsUpgrades
        ] = None,
        velocity_characteristics_upgrades: Optional[
            VelocityCharacteristicsUpgrades
        ] = None,
        weapon_modifiers_upgrades: Optional[WeaponModifiersUpgrades] = None,
    ):
        super().__init__(spaceship_id=spaceship_id)

        if life_characteristics_upgrades is None:
            life_characteristics_upgrades = HealthLifeCharacteristicsUpgrades(0, 0, 0)
        self.life_characteristics_upgrades = life_characteristics_upgrades
        self.life_characteristics_upgrades.changed.connect(
            lambda: self.on_upgrade(self.life_characteristics_upgrades)
        )
        self.life_characteristics_upgrades.changed.connect(
            lambda: self.life_characteristics_upgrades.apply_upgrades(
                self.standard_life_characteristics, self.spaceship.life_characteristics
            )
        )

        if velocity_characteristics_upgrades is None:
            velocity_characteristics_upgrades = VelocityCharacteristicsUpgrades(0, 0, 0)
        self.velocity_characteristics_upgrades = velocity_characteristics_upgrades
        self.velocity_characteristics_upgrades.changed.connect(
            lambda: self.on_upgrade(self.velocity_characteristics_upgrades)
        )
        self.velocity_characteristics_upgrades.changed.connect(
            lambda: self.velocity_characteristics_upgrades.apply_upgrades(
                self.standard_velocity_characteristics,
                self.spaceship.velocity_characteristics,
            )
        )

        if weapon_modifiers_upgrades is None:
            weapon_modifiers_upgrades = WeaponModifiersUpgrades(0, 0, 0, 0, 0)
        self.weapon_modifiers_upgrades = weapon_modifiers_upgrades
        self.weapon_modifiers_upgrades.changed.connect(
            lambda: self.on_upgrade(self.weapon_modifiers_upgrades)
        )
        self.weapon_modifiers_upgrades.changed.connect(
            lambda: self.weapon_modifiers_upgrades.apply_upgrades(
                self.standard_weapon_modifiers, self.spaceship.weapon_modifiers
            )
        )

    def on_upgrade(self, upgrades: Upgrades):
        self.spaceship.pilot.resources -= upgrades.prev_cost

    def can_upgrade_life_characteristics(self) -> bool:
        return self.spaceship.pilot.resources.can_afford(
            self.life_characteristics_upgrades.cost
        )

    def can_upgrade_velocity_characteristics(self) -> bool:
        return self.spaceship.pilot.resources.can_afford(
            self.velocity_characteristics_upgrades.cost
        )

    def can_upgrade_weapon_modifiers(self) -> bool:
        return self.spaceship.pilot.resources.can_afford(
            self.weapon_modifiers_upgrades.cost
        )

    @cached_property
    def standard_life_characteristics(self) -> HealthLifeCharacteristics:
        return self.spaceship.create_life_characteristics()

    @cached_property
    def standard_weapon_modifiers(self) -> WeaponModifiers:
        return self.spaceship.create_weapon_modifiers()

    @cached_property
    def standard_velocity_characteristics(self) -> VelocityCharacteristics:
        return self.spaceship.create_velocity_characteristics()

    def to_dict(self) -> Dict:
        return {
            **super().to_dict(),
            "spaceship_id": self.spaceship_id,
            "life_characteristics_upgrades": self.life_characteristics_upgrades.to_dict(),
            "velocity_characteristics_upgrades": self.velocity_characteristics_upgrades.to_dict(),
            "weapon_modifiers_upgrades": self.weapon_modifiers_upgrades.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "SpaceshipUpgradeSystem":
        return cls(
            spaceship_id=data["spaceship_id"],
            life_characteristics_upgrades=HealthLifeCharacteristicsUpgrades.from_dict(
                data["life_characteristics_upgrades"]
            ),
            weapon_modifiers_upgrades=WeaponModifiersUpgrades.from_dict(
                data["weapon_modifiers_upgrades"]
            ),
            velocity_characteristics_upgrades=VelocityCharacteristicsUpgrades.from_dict(
                data["velocity_characteristics_upgrades"]
            ),
        )


class MinerUpgradeSystem(SpaceshipUpgradeSystem, SpaceshipMixin[MinerMixin]):

    mining_characteristics: MiningCharacteristicsUpgrades

    def __init__(
        self,
        spaceship_id: int,
        life_characteristics_upgrades: Optional[
            HealthLifeCharacteristicsUpgrades
        ] = None,
        velocity_characteristics_upgrades: Optional[WeaponModifiersUpgrades] = None,
        weapon_modifiers_upgrades: Optional[VelocityCharacteristicsUpgrades] = None,
        mining_characteristics: Optional[MiningCharacteristicsUpgrades] = None,
    ):
        super().__init__(
            spaceship_id=spaceship_id,
            life_characteristics_upgrades=life_characteristics_upgrades,
            velocity_characteristics_upgrades=velocity_characteristics_upgrades,
            weapon_modifiers_upgrades=weapon_modifiers_upgrades,
        )
        if mining_characteristics is None:
            mining_characteristics = MiningCharacteristicsUpgrades(0)
        self.mining_characteristics = mining_characteristics
        self.mining_characteristics.changed.connect(
            lambda: self.on_upgrade(self.mining_characteristics)
        )
        self.mining_characteristics.changed.connect(
            lambda: self.mining_characteristics.apply_upgrades(
                self.standard_mining_characteristics,
                self.spaceship.mining_characteristics,
            )
        )

    def can_upgrade_mining_characteristics(self) -> bool:
        return (
            self.spaceship.pilot.resources.can_afford(self.mining_characteristics.cost)
            and self.mining_characteristics.level
            < self.mining_characteristics.config.max_level
        )

    @cached_property
    def standard_mining_characteristics(self) -> MiningCharacteristics:
        return self.spaceship.create_mining_characteristics()
