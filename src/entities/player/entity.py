from src.entities.abstract import GuidedEntity
from src.entities.engines.default_engine import DefaultEngine
from pymunk.vec2d import Vec2d
from .view import PlayerView
from .pilot import PlayerPilot
import pymunk
from src.entities.player.config import *
from ..config import STANDARD_START_HEALTH


class PlayerEntity(GuidedEntity):
    def __init__(self, pos: Vec2d, health, max_health):
        moment = pymunk.moment_for_poly(MASS, VERTICES)
        super().__init__(MASS, moment, body_type=pymunk.Body.DYNAMIC)
        self.pos = pos
        self.shape = pymunk.Poly(self, VERTICES)
        self.pilot = PlayerPilot(self)

        self.control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.control_body.position = pos

        self.pivot = pymunk.PivotJoint(self.control_body, self, (0, 0), (0, 0))
        self.pivot.max_bias = 0  # disable joint correction

        self.engine = DefaultEngine(
            self,
            self.control_body,
            max_speed=MAX_SPEED,
            max_rotation_speed=MAX_ROTATION_SPEED,
            stop_coef=8,
            direct_force=400,
        )
        self.view = PlayerView(self)
        self.max_health = max_health
        self.health = health
        self.is_active = True

    def render(self, screen, camera):
        self.view.draw(screen, camera.dv + self.pos)

    def update(self, dt):
        self.pilot.update(dt)

    def add_to_space(self, space: pymunk.Space):
        space.add(self, self.shape)
        space.add(self.control_body)
        space.add(self.pivot)

    def remove_from_space(self, space: pymunk.Space):
        space.remove(self, self.shape)
        space.remove(self.control_body)
        space.remove(self.pivot)

    def serialize(self) -> str:
        pass

    @staticmethod
    def deserialize(data: str):
        pass

    @staticmethod
    def create_default(pos=Vec2d.zero()):
        return PlayerEntity(pos, STANDARD_START_HEALTH, STANDARD_START_HEALTH)
