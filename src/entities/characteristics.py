import json
from dataclasses import dataclass
from typing import Union, Dict

from src.abstract import Serializable


@dataclass
class VelocityCharacteristics(Serializable):
    rotation_speed: float
    direct_force: float
    max_speed: float
    max_rotation_speed: float
    stop_coef: float
    stop_rotation_coef: float

    def to_dict(self) -> Dict:
        return {
            "rotation_speed": self.rotation_speed,
            "direct_force": self.direct_force,
            "max_speed": self.max_speed,
            "max_rotation_speed": self.max_rotation_speed,
            "stop_coef": self.stop_coef,
            "stop_rotation_coef": self.stop_rotation_coef,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return VelocityCharacteristics(
            rotation_speed=data["rotation_speed"],
            direct_force=data["direct_force"],
            max_speed=data["max_speed"],
            max_rotation_speed=data["max_rotation_speed"],
            stop_coef=data["stop_coef"],
            stop_rotation_coef=data["stop_rotation_coef"],
        )


@dataclass
class WeaponCharacteristics(Serializable):
    weapon_reload_coef: float
    bullet_damage_coef: float
    bullet_distance_coef: float
    bullet_mass_coef: float
    bullet_speed_coef: float

    def to_dict(self) -> Dict:
        return {
            "weapon_reload_coef": self.weapon_reload_coef,
            "bullet_damage_coef": self.bullet_damage_coef,
            "bullet_distance_coef": self.bullet_distance_coef,
            "bullet_mass_coef": self.bullet_mass_coef,
            "bullet_speed_coef": self.bullet_speed_coef,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return WeaponCharacteristics(
            weapon_reload_coef=data["weapon_reload_coef"],
            bullet_damage_coef=data["bullet_damage_coef"],
            bullet_distance_coef=data["bullet_distance_coef"],
            bullet_mass_coef=data["bullet_mass_coef"],
            bullet_speed_coef=data["bullet_speed_coef"],
        )


@dataclass
class LifeCharacteristics(Serializable):
    health: float
    max_health: float
    armor: float

    def decrease(self, damage: float):
        self.health = max(0.0, self.health - damage)

    def increase(self, healing: float):
        self.health = min(healing + self.health, self.max_health)

    def is_alive(self) -> bool:
        return self.health > 0

    def health_fullness(self) -> float:
        return self.health / self.max_health

    def to_dict(self) -> Dict:
        return {
            "health": self.health,
            "max_health": self.max_health,
            "armor": self.armor,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return LifeCharacteristics(
            health=data["health"],
            max_health=data["max_health"],
            armor=data["armor"],
        )
