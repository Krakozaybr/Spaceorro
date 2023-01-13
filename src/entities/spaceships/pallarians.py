from typing import Dict

import pygame
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView
from src.entities.asteroids.abstract import AbstractAsteroid
from src.entities.basic_entity.basic_entity import PolyBasicEntity
from src.entities.basic_entity.basic_spaceship import BasicSpaceship
from src.entities.basic_entity.basic_spaceship import BasicSpaceshipView
from src.entities.basic_entity.health_entity_mixin import HealthEntityMixin
from src.entities.gadgets.engines.abstract import Engine
from src.entities.gadgets.engines.default_engine import DefaultEngine
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.gadgets.health_bars.default_bars import AllyBar
from src.entities.gadgets.weapon.blasters.blaster import Blaster
from src.entities.pilots.abstract import Pilot
from src.entities.pilots.get_pilot import get_pilot
from src.entities.pilots.simple_bot import SimpleBot
from src.entities.spaceships.miner.miner_mixin import MinerMixin
from src.entities.teams import Team
from src.utils.image_manager import ImageManager


class PallariansCruiserView(BasicSpaceshipView):

    entity: HealthEntityMixin
    image = ImageManager().get_pic(ImageManager().PALLARIANS_CRUISER)

    def __init__(self, entity: HealthEntityMixin, *groups: AbstractGroup):
        super().__init__(entity, fps=8, *groups)

    def create_health_bar(self) -> HealthBar:
        return AllyBar(Vec2d(-self.w / 2 - 2, -self.h + 4), self.w + 4)

    def draw_health_bar(self, screen: pygame.Surface, pos: Vec2d):
        self.health_bar.render(
            screen,
            self.entity.life_characteristics,
            pos,
        )


class PallariansCruiser(MinerMixin, PolyBasicEntity):

    # static fields
    config_name = "pallarians_cruiser.json"
    start_config_name = "pallarians_cruiser.json"

    def create_engine(self) -> Engine:
        return DefaultEngine(self, self.control_body, self.velocity_characteristics)

    def create_view(self) -> EntityView:
        return PallariansCruiserView(self)

    def create_weapon(self) -> Blaster:
        return Blaster.create_simple_blaster(self)

    def create_pilot(self) -> Pilot:
        return SimpleBot(self, Team.neutral)

    def on_explode(self):
        pass

    def to_dict(self) -> Dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: Dict):
        res = PallariansCruiser(
            weapon=Blaster.from_dict(data["weapon"]), **cls.get_default_params(data)
        )
        res.pilot = get_pilot(data["pilot"])
        res.apply_params_to_bodies(data)
        return res
