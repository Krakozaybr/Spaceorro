from src.entities.abstract import PhysicEntity
from src.entities.engines.default_engine import DefaultEngine
from pymunk.vec2d import Vec2d
from .view import PlayerView
import pymunk


MASS = 1000
# TODO
VERTICES = []


class PlayerEntity(PhysicEntity):
    def __init__(self, pos: Vec2d, health, max_health):
        moment = pymunk.moment_for_poly(MASS, VERTICES)
        super().__init__(MASS, moment, body_type=pymunk.Body.DYNAMIC)
        self.pos = pos
        self.shape = pymunk.Poly(self, VERTICES)
        self.engine = DefaultEngine(self)
        self.view = PlayerView()
        self.max_health = max_health
        self.health = health
        self.is_active = True

    def render(self, screen, camera):
        self.view.draw(screen, camera.dv + self.pos)

    def update(self, dt):
        pass

    def serialize(self) -> str:
        pass

    @staticmethod
    def deserialize(data: str):
        pass
