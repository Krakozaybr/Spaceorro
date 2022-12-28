from math import inf

from src.entities.abstract import GuidedEntity, HealthBar
from src.entities.gadgets.engines.default_engine import DefaultEngine
from pymunk.vec2d import Vec2d
from .view import PlayerView
from .pilot import PlayerPilot
import pymunk
from src.entities.config.default_config import DefaultEntityConfig
from src.entities.gadgets.health_bars.default_bars import AllyBar


CONFIG_NAME = "player.json"
config = DefaultEntityConfig(CONFIG_NAME)


class PlayerEntity(GuidedEntity):
    def __init__(self, pos: Vec2d, health, max_health):
        # Pymunk
        moment = pymunk.moment_for_poly(config.MASS, config.VERTICES)
        super().__init__(config.MASS, moment, body_type=pymunk.Body.DYNAMIC)

        self.position = pos
        self.shape = pymunk.Poly(self, config.VERTICES)

        self.control_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.control_body.position = pos

        self.pivot = pymunk.PivotJoint(self.control_body, self, (0, 0), (0, 0))
        self.pivot.max_bias = 0  # disable joint correction

        # Instruments
        self.engine = DefaultEngine(
            self,
            self.control_body,
            max_speed=config.MAX_SPEED,
            max_rotation_speed=config.MAX_ROTATION_SPEED,
            stop_coef=8,
            stop_rotation_coef=10,
            direct_force=400,
        )
        self.pilot = PlayerPilot(self)
        self.view = PlayerView(self)
        self.health_bar = AllyBar(
            Vec2d(-config.WIDTH / 2 - 2, -config.HEIGHT + 4), config.WIDTH + 4, 8
        )

        # Standard characteristics
        self.max_health = max_health
        self.health = health
        self.is_active = True
        self.is_alive = True

    def render(self, screen, camera):
        self.view.draw(screen, camera.dv + self.position)
        self.health_bar.render(
            screen, self.health / self.max_health, camera.dv + self.position
        )

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
        return PlayerEntity(
            pos, config.STANDARD_START_HEALTH, config.STANDARD_START_HEALTH
        )
