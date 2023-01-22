from typing import Dict, Optional

import pymunk
from pymunk import Vec2d

from src.entities.abstract.abstract import Entity
from src.entities.abstract.guided_entity import AbstractSpaceship
from src.entities.basic_entity.basic_spaceship import BasicSpaceshipMixin
from src.entities.basic_entity.explosive import Explosive
from src.entities.gadgets.weapon.bullets.abstract import AbstractBullet
from src.entities.gadgets.weapon.bullets.view import BlasterChargeView
from src.entities.modifiers_and_characteristics import (
    TemporaryObjectLifeCharacteristics,
    WeaponModifiers,
)
from src.entities.pickupable.abstract import Pickupable
from src.entities.teams import Team
from src.environment.abstract import get_environment
from src.utils.sound_manager import SoundManager

CONFIG_NAME = "blaster_charge.json"


class BlasterCharge(AbstractBullet, Explosive):

    config_name = "blaster_charge.json"
    life_characteristics: TemporaryObjectLifeCharacteristics
    view: BlasterChargeView

    def __init__(
        self,
        level: int,
        spaceship_id: int,
        pos: Vec2d,
        direction: Optional[Vec2d] = Vec2d.zero(),
        angle: Optional[float] = 0.0,
        life_characteristics: Optional[TemporaryObjectLifeCharacteristics] = None,
        weapon_modifiers: Optional[WeaponModifiers] = None,
        team: Optional[Team] = Team.neutral,
    ):
        self.level = level
        BasicSpaceshipMixin.__init__(self, spaceship_id)
        self.team = team

        if weapon_modifiers is not None:
            self._modifiers = weapon_modifiers

        Explosive.__init__(
            self,
            pos=pos,
            life_characteristics=life_characteristics,
        )
        self.angle = angle
        self.control_body.velocity = direction.normalized() * self.characteristics.speed
        self.direction = direction
        self.exploding = False

    def create_life_characteristics(self) -> TemporaryObjectLifeCharacteristics:
        return TemporaryObjectLifeCharacteristics(
            life_time=self.config.life_time * self.modifiers.bullet_life_time_coef
        )

    def create_moment(self) -> float:
        return pymunk.moment_for_circle(self.config.mass, 0, self.config.radius)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Circle(None, self.config.radius)

    def update(self, dt: float):
        super().update(dt)
        self.life_characteristics.decrease(dt)

    def on_explode(self):
        env = get_environment()
        sender = self if self.spaceship is None else self.spaceship
        for entity in env.get_entities_near(
            self.position, self.characteristics.explosion_radius
        ):
            entity.take_damage(self.characteristics.damage, sender)

    def die(self):
        self.life_characteristics.decrease(self.life_characteristics.life_time)

    def collide(self, other: Entity):
        if not isinstance(other, Pickupable):
            self.explode()

    def take_damage(self, damage: float, sender: "Entity") -> None:
        self.life_characteristics.decrease(self.life_characteristics.life_time)

    def create_view(self) -> BlasterChargeView:
        return BlasterChargeView(self, self.config.image)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            "life_characteristics": TemporaryObjectLifeCharacteristics.from_dict(
                data["life_characteristics"]
            ),
        }

    def to_dict(self) -> Dict:
        data = {
            "level": self.level,
            "spaceship_id": self.spaceship_id,
        }
        if not self.spaceship_exists:
            data["weapon_modifiers"] = self.modifiers
        return {**super().characteristics_to_dict(), **super().to_dict(), **data}

    @classmethod
    def from_dict(cls, data: Dict):
        res = BlasterCharge(
            level=data["level"],
            spaceship_id=data["spaceship_id"],
            pos=data["body"]["position"],
            **cls.get_characteristics(data)
        )
        res.in_space = False
        res.apply_params_to_bodies(data)
        return res

    @classmethod
    def new(cls, master: AbstractSpaceship, dpos: Vec2d, direction: Vec2d):
        bullet_level = 0
        for level in cls.configs:
            if level > master.weapon_modifiers.weapon_level:
                break
            bullet_level = level
        pos = (
            master.position
            + dpos
            + dpos.normalized() * cls.configs[bullet_level].radius
        )
        return cls(
            spaceship_id=master.obj_id,
            pos=pos,
            angle=master.angle,
            level=bullet_level,
            direction=direction,
            team=master.team,
        )
