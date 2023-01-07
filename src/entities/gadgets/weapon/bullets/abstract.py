from abc import ABC, abstractmethod
from typing import Dict

from pymunk import Vec2d

from src.entities.abstract.abstract import SaveStrategy
from src.entities.abstract.guided_entity import AbstractSpaceship
from src.entities.basic_entity.basic_entity import BasicEntity
from src.entities.basic_entity.basic_spaceship import SpaceshipMixin
from src.entities.entity_configs import BulletEntityConfig
from src.entities.modifiers_and_characteristics import (
    WeaponModifiers,
    BulletCharacteristics,
)
from src.entities.teams import Team
from src.settings import get_bullet_configs


class AbstractBullet(BasicEntity, SpaceshipMixin, ABC):

    # static fields
    configs: Dict[int, BulletEntityConfig]
    save_strategy = SaveStrategy.DEPENDED

    # non-static fields
    spaceship_id: int
    level: int
    team: Team
    _characteristics: BulletCharacteristics
    _modifiers: WeaponModifiers = None
    _config: BulletEntityConfig

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.configs = {
            data["level"]: BulletEntityConfig.from_dict(data)
            for data in get_bullet_configs(cls.config_name)
        }

    @property
    def damage(self):
        return self.characteristics.damage * self.modifiers.bullet_damage_coef

    @property
    def modifiers(self) -> WeaponModifiers:
        if hasattr(self, "_modifiers"):
            self._modifiers = self.spaceship.weapon_modifiers
        return self._modifiers

    @property
    def config(self) -> BulletEntityConfig:
        if not hasattr(self, "_config"):
            self._config = self.configs[self.level]
        return self._config

    @property
    def characteristics(self) -> BulletCharacteristics:
        if not hasattr(self, "_characteristics"):
            self._characteristics = BulletCharacteristics(
                damage=self.config.damage * self.modifiers.bullet_damage_coef,
                speed=self.config.speed * self.modifiers.bullet_speed_coef,
                explosion_radius=self.config.explosion_radius + self.config.radius,
            )
        return self._characteristics

    @classmethod
    @abstractmethod
    def new(cls, master: AbstractSpaceship, dpos: Vec2d, direction: Vec2d):
        pass
