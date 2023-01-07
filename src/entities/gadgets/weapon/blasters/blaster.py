from dataclasses import dataclass
from typing import Type, Optional, List, Dict

from pymunk import Vec2d

from src.entities.basic_entity.basic_spaceship import BasicSpaceship
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.gadgets.weapon.bullets import find_bullet_cls_by_name
from src.entities.gadgets.weapon.bullets.abstract import (
    AbstractBullet,
)
from src.entities.gadgets.weapon.weapon_modifiers_mixin import WeaponModifiersMixin
from src.settings import get_blaster_characteristics
from src.utils.serializable_dataclass import SerializableDataclass


@dataclass
class BlasterConfig(SerializableDataclass):
    full_reload_time: float
    bullet_types: List[Type[AbstractBullet]]

    special_fields_serializing = {
        "bullet_types": lambda val: BlasterConfig.serialize_bullet_type(val)
    }
    special_fields_deserializing = {
        "bullet_types": lambda val: BlasterConfig.deserialize_bullet_type(val)
    }

    @classmethod
    def serialize_bullet_type(cls, val: List[Type[AbstractBullet]]):
        return [bt.__class__.__name__ for bt in val]

    @classmethod
    def deserialize_bullet_type(cls, bts: List[str]):
        return [find_bullet_cls_by_name(name) for name in bts]


class Blaster(AbstractStateWeapon, WeaponModifiersMixin):
    config: BlasterConfig
    reload_time: float
    current_bullet_type: int
    config_name: str

    def __init__(
        self,
        master_id: int,
        config_name: str,
        reload_time: Optional[float] = 0.0,
        current_bullet_type: Optional[int] = 0,
    ):
        WeaponModifiersMixin.__init__(self, master_id)
        self.config_name = config_name
        self.config = BlasterConfig.from_dict(get_blaster_characteristics(config_name))
        self.reload_time = reload_time
        self.current_bullet_type = current_bullet_type

    def shoot(self, pos: Vec2d) -> bool:
        if self.can_shoot():
            dpos = Vec2d(*self.spaceship.config.blaster_relative_position).rotated(
                self.spaceship.angle
            )
            bt = self.config.bullet_types[self.current_bullet_type]
            self.entity_registrator.add_entity(
                bt.new(
                    master=self.spaceship,
                    dpos=dpos,
                    direction=pos,
                )
            )
            self.reload_time = self.full_reload_time
            return True
        return False

    @property
    def full_reload_time(self) -> float:
        return self.config.full_reload_time / self.modifiers.weapon_reload_coef

    def can_shoot(self) -> bool:
        return not self.reload_time

    def update(self, dt: float) -> None:
        self.reload_time = max(0.0, self.reload_time - dt)

    def to_dict(self) -> Dict:
        return {
            **super().to_dict(),
            "master_id": self.spaceship_id,
            "reload_time": self.reload_time,
            "config_name": self.config_name,
            "current_bullet_type": self.current_bullet_type,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            master_id=data["master_id"],
            reload_time=data["reload_time"],
            config_name=data["config_name"],
            current_bullet_type=data["current_bullet_type"],
        )

    @staticmethod
    def create_simple_blaster(master: BasicSpaceship):
        return Blaster(
            master_id=master.id,
            config_name="simple_blaster.json",
        )
