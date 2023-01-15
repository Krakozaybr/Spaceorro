import inspect
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.abstract import Serializable
from src.entities.pilots.abstract import Pilot
from src.entities.abstract.abstract import SaveStrategy, Entity
from src.entities.abstract.guided_entity import AbstractSpaceship
from src.entities.basic_entity.basic_entity import BasicEntity, EntityWithFixedMass
from src.entities.basic_entity.explosive import Explosive, ExplosiveView
from src.entities.basic_entity.health_entity_mixin import HealthEntityMixin
from src.entities.basic_entity.view import PolyBasicView, HealthBarMixin
from src.entities.entity_configs import SpaceshipEntityConfig
from src.entities.gadgets.engines.abstract import Engine
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.modifiers_and_characteristics import (
    WeaponModifiers,
    VelocityCharacteristics,
    HealthLifeCharacteristics,
)
from src.entities.pickupable.abstract import Pickupable
from src.entities.teams import Team
from src.settings import get_entity_start_config
from src.utils.body_serialization import *


class BasicSpaceshipView(PolyBasicView, HealthBarMixin, ExplosiveView, ABC):
    def __init__(self, entity: Entity, fps: Optional[int] = 1, *groups: AbstractGroup):
        PolyBasicView.__init__(self, entity=entity, *groups)
        ExplosiveView.__init__(
            self, entity=entity, explosion_radius=max(self.w, self.h), fps=fps, *groups
        )
        HealthBarMixin.__init__(self, entity=entity, *groups)


class BasicSpaceship(
    AbstractSpaceship, Explosive, EntityWithFixedMass, HealthEntityMixin, ABC
):

    save_strategy = SaveStrategy.ENTITY

    life_characteristics: HealthLifeCharacteristics
    start_config_name: str
    weapon: AbstractStateWeapon
    start_config: Dict
    config: SpaceshipEntityConfig
    config_name: str

    def __init__(
        self,
        pos: Vec2d,
        weapon_modifiers: Optional[WeaponModifiers] = None,
        velocity_characteristics: Optional[VelocityCharacteristics] = None,
        life_characteristics: Optional[HealthLifeCharacteristics] = None,
        mass: Optional[float] = None,
        moment: Optional[float] = None,
        weapon: Optional[AbstractStateWeapon] = None,
        entity_id: Optional[int] = None,
        pilot: Optional[Pilot] = None,
    ):
        Explosive.__init__(
            self,
            pos=pos,
            life_characteristics=life_characteristics,
            mass=mass,
            moment=moment,
            entity_id=entity_id,
        )

        # Characteristics
        if weapon_modifiers is None:
            weapon_modifiers = self.create_weapon_modifiers()
        self.weapon_modifiers = weapon_modifiers

        if velocity_characteristics is None:
            velocity_characteristics = self.create_velocity_characteristics()
        self.velocity_characteristics = velocity_characteristics

        # Instruments
        self.engine = self.create_engine()
        if pilot is None:
            pilot = self.create_pilot()
        self.pilot = pilot
        if weapon is None:
            weapon = self.create_weapon()
        self.weapon = weapon

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            cls.start_config = get_entity_start_config(cls.start_config_name)
            cls.config = SpaceshipEntityConfig.load(cls.config_name)

    @property
    def team(self) -> Team:
        return self.pilot.team

    def collide(self, other: Entity):
        super().collide(other)
        if isinstance(other, Pickupable):
            self.pilot.pick_up(other)
            other.die()

    def take_damage(self, damage: float, sender: 'Entity') -> None:
        super().take_damage(damage, sender)
        self.life_characteristics.decrease(damage)

    @abstractmethod
    def create_weapon(self) -> AbstractStateWeapon:
        pass

    @abstractmethod
    def create_engine(self) -> Engine:
        pass

    @abstractmethod
    def create_pilot(self) -> Pilot:
        pass

    def die(self):
        super().die()
        self.life_characteristics.decrease(self.life_characteristics.health)

    def shoot(self):
        if self.is_alive:
            self.weapon.shoot(Vec2d(0, -1).rotated(self.angle))

    def create_life_characteristics(self) -> HealthLifeCharacteristics:
        return HealthLifeCharacteristics.from_dict(
            self.start_config["life_characteristics"]
        )

    def create_weapon_modifiers(self) -> WeaponModifiers:
        return WeaponModifiers.from_dict(self.start_config["weapon_modifiers"])

    def create_velocity_characteristics(self) -> VelocityCharacteristics:
        return VelocityCharacteristics.from_dict(
            self.start_config["velocity_characteristics"]
        )

    def update(self, dt) -> None:
        super().update(dt)
        self.pilot.update(dt)
        self.weapon.update(dt)
        self.engine.update(dt)

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            "velocity_characteristics": VelocityCharacteristics.from_dict(
                data["velocity_characteristics"]
            ),
            "weapon_modifiers": WeaponModifiers.from_dict(data["weapon_modifiers"]),
            "life_characteristics": HealthLifeCharacteristics.from_dict(
                data["life_characteristics"]
            ),
        }

    def characteristics_to_dict(self) -> Dict:
        return {
            "velocity_characteristics": self.velocity_characteristics.to_dict(),
            "weapon_modifiers": self.weapon_modifiers.to_dict(),
            **BasicEntity.characteristics_to_dict(self),
        }

    def to_dict(self) -> Dict:
        data = BasicEntity.to_dict(self)
        return {
            "weapon": self.weapon.to_dict(),
            "pilot": self.pilot.to_dict(),
            **data,
        }

    @classmethod
    def create_default(cls, pos=Vec2d.zero()):
        return cls(pos=pos)


Spaceship = TypeVar("Spaceship", bound=BasicSpaceship)


class SpaceshipMixin(Generic[Spaceship]):
    _spaceship: Spaceship
    spaceship_id: int

    def __init__(self, spaceship_id: int):
        self.spaceship_id = spaceship_id

    @property
    def spaceship(self) -> Spaceship:
        if not hasattr(self, "_spaceship") or self._spaceship is None:
            self._spaceship = Entity.store[self.spaceship_id]
        return self._spaceship

    @spaceship.setter
    def spaceship(self, val: Spaceship) -> None:
        self._spaceship = val
        self.spaceship_id = val.id

    @property
    def spaceship_exists(self):
        return self.spaceship is not None


class BasicSpaceshipMixin(SpaceshipMixin[BasicSpaceship]):
    pass
