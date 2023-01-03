from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.utils.serializable_dataclass import SerializableDataclass


@dataclass
class VelocityCharacteristics(SerializableDataclass):
    rotation_speed: float
    direct_force: float
    max_speed: float
    max_rotation_speed: float
    stop_coef: float
    stop_rotation_coef: float


@dataclass
class WeaponModifiers(SerializableDataclass):
    weapon_level: int
    weapon_reload_coef: float
    bullet_damage_coef: float
    bullet_life_time_coef: float
    bullet_mass_coef: float
    bullet_speed_coef: float


class LifeCharacteristics(SerializableDataclass, ABC):
    @abstractmethod
    def is_alive(self) -> bool:
        pass


@dataclass
class HealthLifeCharacteristics(LifeCharacteristics):
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


@dataclass
class BulletLifeCharacteristics(LifeCharacteristics):
    life_time: float

    def decrease(self, dt: float):
        self.life_time = max(0.0, self.life_time - dt)

    def is_alive(self) -> bool:
        return self.life_time > 0


@dataclass
class BulletCharacteristics(SerializableDataclass):
    damage: float
    speed: float
    explosion_radius: float
