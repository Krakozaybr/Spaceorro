from pymunk import Vec2d

from src.entities.entities_impls.basic_entity.view import BasicView
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.gadgets.health_bars.default_bars import AllyBar


# TODO image
class PlayerView(BasicView):
    def create_health_bar(self) -> HealthBar:
        return AllyBar(Vec2d(-self.w / 2 - 2, -self.h + 4), self.w + 4, 8)
