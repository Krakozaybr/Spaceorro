from src.entities.abstract import Pilot
from .view import PlayerView
from .entity import PlayerEntity
from src.entities.config import STANDARD_START_HEALTH


class PlayerPilot(Pilot):
    def __init__(self, pos):
        self.entity = PlayerEntity(pos, STANDARD_START_HEALTH, STANDARD_START_HEALTH)

    def catch_event(self, e):
        ...

    def render(self, screen, camera):
        self.entity.render(screen, camera)

    def update(self, dt):
        pass
