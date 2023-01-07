from typing import Dict, Optional

import pymunk
from pymunk import Vec2d

from src.entities.abstract.abstract import Entity, SaveStrategy
from src.entities.abstract.guided_entity import AbstractSpaceship
from src.entities.basic_entity.basic_entity import BasicEntity
from src.entities.basic_entity.basic_spaceship import SpaceshipMixin
from src.entities.gadgets.weapon.bullets import AbstractBullet
from src.entities.gadgets.weapon.bullets.view import BlasterChargeView
from src.entities.modifiers_and_characteristics import (
    BulletLifeCharacteristics,
)
from src.environment.abstract import get_environment
from src.utils.body_serialization import (
    apply_params_to_dynamic_body_from_dict,
    apply_params_to_kinematic_body_from_dict,
)

CONFIG_NAME = "blaster_charge.json"


class BlasterCharge(AbstractBullet):

    config_name = "blaster_charge.json"
    life_characteristics: BulletLifeCharacteristics
    exploding: bool
    view: BlasterChargeView

    def __init__(
        self,
        level: int,
        spaceship_id: int,
        direction: Optional[Vec2d] = Vec2d.zero(),
        angle: Optional[float] = 0.0,
        pos: Optional[Vec2d] = None,
        dpos: Optional[Vec2d] = None,
        life_characteristics: Optional[BulletLifeCharacteristics] = None,
    ):
        self.level = level
        SpaceshipMixin.__init__(self, spaceship_id)
        self.team = self.spaceship.team
        if pos is None:
            pos = (
                self.spaceship.position + dpos + dpos.normalized() * self.config.radius
            )
        BasicEntity.__init__(
            self,
            pos,
            life_characteristics,
        )
        self.angle = angle
        self.control_body.velocity = direction.normalized() * self.characteristics.speed
        self.direction = direction
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
        print("saved blaster charge")
        return {
            "level": self.level,
            "spaceship_id": self.spaceship_id,
            **self.characteristics_to_dict(),
            **super().to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        print(cls.__name__, "inited")
        res = BlasterCharge(
            level=data["level"],
            spaceship_id=data["spaceship_id"],
            pos=data["body"]["position"],
            **cls.get_characteristics(data)
        )
        body = data["body"]
        control_body = data["control_body"]
        res.in_space = False
        apply_params_to_dynamic_body_from_dict(res, body)
        apply_params_to_kinematic_body_from_dict(res.control_body, control_body)
        return res

    @classmethod
    def new(cls, master: AbstractSpaceship, dpos: Vec2d, direction: Vec2d):
        bullet_level = 0
        for level in cls.configs:
            if level > master.weapon_modifiers.weapon_level:
                break
            bullet_level = level
        return cls(
            spaceship_id=master.id,
            dpos=dpos,
            angle=master.angle,
            level=bullet_level,
            direction=direction,
        )
