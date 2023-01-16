from abc import ABC
from typing import Dict

import pygame
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView
from src.entities.basic_entity.basic_entity import PolyBasicEntity
from src.entities.basic_entity.basic_spaceship import BasicSpaceship, BasicSpaceshipView
from src.entities.basic_entity.mixins.upgradeable_miner_mixin import (
    UpgradeableMinerMixin,
)
from src.entities.gadgets.engines.abstract import Engine
from src.entities.gadgets.engines.default_engine import DefaultEngine
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.gadgets.health_bars.default_bars import AllyBar, EnemyBar
from src.entities.gadgets.weapon.abstract_weapon import AbstractStateWeapon
from src.entities.gadgets.weapon.blasters.blaster import Blaster
from src.entities.pilots.abstract import Pilot
from src.entities.pilots.get_pilot import get_pilot
from src.entities.pilots.simple_bot import SimpleBot
from src.entities.teams import Team


class TeamMixin(UpgradeableMinerMixin, PolyBasicEntity, ABC):
    spaceship_team: Team

    def create_pilot(self) -> Pilot:
        return SimpleBot(self, self.spaceship_team)


class DefaultSpaceshipView(BasicSpaceshipView, ABC):

    entity: BasicSpaceship
    image: pygame.Surface

    def __init__(self, entity: BasicSpaceship, *groups: AbstractGroup):
        super().__init__(entity, fps=8, *groups)

    def create_health_bar(self) -> HealthBar:
        if self.entity.team == Team.player:
            return AllyBar(Vec2d(-self.w / 2 - 2, -self.h + 4), self.w + 4)
        else:
            return EnemyBar(Vec2d(-self.w / 2 - 2, -self.h + 4), self.w + 4)

    def draw_health_bar(self, screen: pygame.Surface, pos: Vec2d):
        self.health_bar.render(
            screen,
            self.entity.life_characteristics,
            pos,
        )


def create_view(
    src_image: pygame.Surface, entity: BasicSpaceship, *groups: AbstractGroup
):
    class Impl(DefaultSpaceshipView):
        image = src_image

    return Impl(entity, *groups)


class DefaultSpaceship(UpgradeableMinerMixin, PolyBasicEntity, ABC):
    # static fields
    config_name: str
    start_config_name: str

    def create_engine(self) -> Engine:
        return DefaultEngine(self, self.control_body, self.velocity_characteristics)

    def create_weapon(self) -> Blaster:
        return Blaster.create_simple_blaster(self)

    def on_explode(self):
        pass

    def to_dict(self) -> Dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: Dict):
        res = cls(
            weapon=Blaster.from_dict(data["weapon"]), **cls.get_default_params(data)
        )
        res.pilot = get_pilot(data["pilot"])
        res.apply_params_to_bodies(data)
        return res


# class Drone(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
#
#
# class Corvette(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
#
#
# class Miner(Corvette):
#     pass
#
#
# class Destroyer(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
#
#
# class Cruiser(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
#
#
# class Trader(Cruiser):
#     pass
#
#
# class Battleship(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
#
#
# class Dreadnought(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
#
#
# class Mothership(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
#
#
# class DroneBase(DefaultSpaceship):
#     def create_weapon(self) -> AbstractStateWeapon:
#         pass
#
#     def create_engine(self) -> Engine:
#         pass
#
#     def create_pilot(self) -> Pilot:
#         pass
#
#     def on_explode(self):
#         pass
#
#     def create_moment(self) -> float:
#         pass
#
#     def create_shape(self) -> pymunk.Shape:
#         pass
#
#     def create_view(self) -> EntityView:
#         pass
#
#     @classmethod
#     def from_dict(cls, data: Dict):
#         pass
