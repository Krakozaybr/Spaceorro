from src.entities.abstract import Entity
from src.entities.engines.default_engine import DefaultEngine
from src.utils.vector import Vector
from .view import PlayerView
import pymunk


MASS = 1000


class PlayerEntity(Entity):
    def __init__(self, pos: Vector, health, max_health):
        self.pos = pos
        self.body = pymunk.Body(mass=MASS, moment=0, body_type=pymunk.Body.DYNAMIC)
        # TODO shape
        self.shape = ...
        self.engine = DefaultEngine()
        self.view = PlayerView()
        self.max_health = max_health
        self.health = health

    def render(self, screen, camera):
        self.view.draw(screen, camera.dv + self.pos)

    def update(self, dt):
        pass
