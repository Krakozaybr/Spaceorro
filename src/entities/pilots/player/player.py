import math
from typing import Dict, Optional

from pymunk.vec2d import Vec2d

from src.entities.asteroids.abstract import AbstractAsteroid
from src.entities.basic_entity.mixins.upgradeable_miner_mixin import (
    UpgradeableMinerMixin,
)
from src.entities.basic_entity.mixins.upgradeable_spaceship_mixin import (
    UpgradeableSpaceshipMixin,
)
from src.entities.pilots.basic_pilot import BasicPilot
from src.entities.pilots.player.controls_config import *
from src.entities.spaceships.miner.miner_mixin import MinerMixin
from src.entities.teams import Team
from src.environment.abstract import get_environment
from src.resources import Resources
from src.settings import W, H


class PlayerPilot(BasicPilot):

    entity: UpgradeableSpaceshipMixin

    def __init__(
        self,
        entity: Optional[UpgradeableSpaceshipMixin] = None,
        _id: Optional[int] = None,
        resources: Optional[Resources] = None,
    ):
        super().__init__(entity=entity, _id=_id, resources=resources, team=Team.player)

    def set_spaceship(self, spaceship: UpgradeableSpaceshipMixin):
        self.entity = spaceship
        spaceship.pilot = self

    def update(self, dt: float):
        controls = Controls()

        up = controls.is_key_pressed(GO_UP)
        down = controls.is_key_pressed(GO_DOWN)
        left = controls.is_key_pressed(GO_LEFT)
        right = controls.is_key_pressed(GO_RIGHT)
        rotate_clockwise = controls.is_key_pressed(ROTATE_CLOCKWISE)
        rotate_counterclockwise = controls.is_key_pressed(ROTATE_COUNTERCLOCKWISE)

        mouse_pos = controls.get_mouse_pos() - Vec2d(W / 2, H / 2)

        if isinstance(self.entity, MinerMixin):
            if controls.is_mouse_pressed(MINE):
                env = get_environment()
                asteroid = env.get_entity_at(self.entity.position + mouse_pos)
                if not isinstance(asteroid, AbstractAsteroid):
                    asteroid = None
                else:
                    self.toast.emit("Mining")
                self.entity.drill.set_target(asteroid)
            else:
                self.entity.drill.set_target(None)

        if controls.is_key_pressed(FIRE):
            self.entity.shoot()
            self.toast.emit("Shoot")
        if controls.is_key_just_up(pygame.K_u) and isinstance(
            self.entity, UpgradeableMinerMixin
        ):
            self.entity.upgrade_system.mining_characteristics.upgrade_level()

        if up:
            self.entity.engine.apply_force(Vec2d(0, -1), dt)
        if down:
            self.entity.engine.apply_force(Vec2d(0, 1), dt)
        if left:
            self.entity.engine.apply_force(Vec2d(-1, 0), dt)
        if right:
            self.entity.engine.apply_force(Vec2d(1, 0), dt)
        if rotate_clockwise:
            self.entity.engine.rotate_clockwise(dt, 0.1)
        if rotate_counterclockwise:
            self.entity.engine.rotate_counterclockwise(dt, 0.1)

        angle = mouse_pos.angle
        self.entity.engine.rotate_to(dt, (angle + math.pi / 2) % (math.pi * 2))

        self.entity.engine.stop(dt * 0.4, not (up or down), not (left or right), False)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**super().get_default_params(data))
