from typing import Dict, Optional

import pymunk
from pymunk import Vec2d

from src.entities.abstract.abstract import Entity
from src.entities.abstract.guided_entity import GuidedEntity
from src.entities.basic_entity.basic_entity import BasicEntity
from src.entities.basic_entity.basic_spaceship import MasterMixin
from src.entities.gadgets.weapon.bullets import AbstractBullet
from src.entities.gadgets.weapon.bullets.view import BlasterChargeView
from src.entities.modifiers_and_characteristics import (
    BulletLifeCharacteristics,
)
from src.environment.abstract import get_environment

CONFIG_NAME = "blaster_charge.json"


class BlasterCharge(AbstractBullet):

    config_name = "blaster_charge.json"
    life_characteristics: BulletLifeCharacteristics
    exploding: bool
    view: BlasterChargeView

    def __init__(
        self,
        level: int,
        master_id: int,
        direction: Vec2d,
        angle: float,
        pos: Optional[Vec2d] = None,
        dpos: Optional[Vec2d] = None,
        life_characteristics: Optional[BulletLifeCharacteristics] = None,
    ):
        assert pos is not None or dpos is not None
        assert pos is None or dpos is None

        self.level = level
        MasterMixin.__init__(self, master_id)
        if pos is None:
            pos = self.master.position + dpos + dpos.normalized() * self.config.radius
        BasicEntity.__init__(
            self,
            pos,
            life_characteristics,
        )
        self.angle = angle
        self.control_body.velocity = direction.normalized() * self.characteristics.speed
        self.exploding = False

    def create_life_characteristics(self) -> BulletLifeCharacteristics:
        return BulletLifeCharacteristics(
            life_time=self.config.life_time * self.modifiers.bullet_life_time_coef
        )

    def create_moment(self) -> float:
        return pymunk.moment_for_circle(self.config.mass, 0, self.config.radius)

    def create_shape(self) -> pymunk.Shape:
        return pymunk.Circle(self, self.config.radius)

    def update(self, dt: float):
        self.life_characteristics.decrease(dt)
        self.view.update(dt)
        if not self.exploding and not self.is_alive:
            self.explode()
        if self.exploding and self.view.animation_passed:
            self.is_active = False

    def explode(self):
        self.control_body.velocity = Vec2d.zero()
        self.life_characteristics.decrease(self.life_characteristics.life_time)
        self.exploding = True
        self.view.start_exposing()
        env = get_environment()
        for entity in env.get_entities_near(
            self.position, self.characteristics.explosion_radius
        ):
            entity.take_damage(self.characteristics.damage)

    def collide(self, other: Entity):
        self.explode()

    def take_damage(self, damage: float):
        self.life_characteristics.decrease(self.life_characteristics.life_time)

    def create_view(self) -> BlasterChargeView:
        return BlasterChargeView(self, self.config.image)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            "life_characteristics": BulletLifeCharacteristics.from_dict(
                data["life_characteristics"]
            ),
        }

    def to_dict(self) -> Dict:
        return {
            "level": self.level,
            "master_id": self.master_id,
            "pos": self.position,
            "angle": self.angle,
            **self.characteristics_to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return BlasterCharge(
            level=data["level"],
            master_id=data["master_id"],
            pos=data["pos"],
            angle=data["angle"],
            **cls.get_characteristics(data)
        )

    @classmethod
    def new(cls, master: GuidedEntity, dpos: Vec2d, direction: Vec2d):
        bullet_level = 0
        for level in cls.configs:
            if level > master.weapon_modifiers.weapon_level:
                break
            bullet_level = level
        return cls(
            master_id=master.id,
            dpos=dpos,
            angle=master.angle,
            level=bullet_level,
            direction=direction,
        )
