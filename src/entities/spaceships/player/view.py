import pygame
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.basic_entity.health_entity_mixin import HealthEntityMixin
from src.entities.basic_entity.view import PolyBasicView
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.gadgets.health_bars.default_bars import AllyBar


# TODO image
class PlayerView(PolyBasicView):

    entity: HealthEntityMixin

    def __init__(self, entity: HealthEntityMixin, *groups: AbstractGroup):
        super().__init__(entity, *groups)

    def create_health_bar(self) -> HealthBar:
        return AllyBar(Vec2d(-self.w / 2 - 2, -self.h + 4), self.w + 4, 8)

    def draw_health_bar(self, screen: pygame.Surface, pos: Vec2d):
        self.health_bar.render(
            screen,
            self.entity.life_characteristics.health_fullness(),
            pos,
        )
