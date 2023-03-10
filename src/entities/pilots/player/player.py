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
from src.entities.pickupable.abstract import Pickupable
from src.entities.pickupable.resource import PickupableResource
from src.entities.pilots.basic_pilot import BasicPilot
from src.entities.pilots.player.controls_config import *
from src.entities.spaceships.miner.miner_mixin import MinerMixin
from src.entities.teams import Team
from src.environment.abstract import get_environment
from src.resources import Resources
from src.settings import W, H
from src.utils.sound_manager import SoundManager


class PlayerPilot(BasicPilot):

    entity: UpgradeableSpaceshipMixin

    def __init__(
        self,
        entity: Optional[UpgradeableSpaceshipMixin] = None,
        _obj_id: Optional[int] = None,
        resources: Optional[Resources] = None,
        score: float = 0,
    ):
        super().__init__(
            entity=entity, _obj_id=_obj_id, resources=resources, team=Team.player
        )
        self.score = score

    def set_spaceship(self, spaceship: UpgradeableSpaceshipMixin):
        if self.entity is not None:
            try:
                self.entity.on_damage.remove(SoundManager().play_bullet_sound)
            except ValueError:
                # case of deserializing
                pass
        self.entity = spaceship
        self.entity.on_damage.connect(self.on_damage_sound)
        self.entity.on_death.connect(self.on_death_sound)
        spaceship.pilot = self
        spaceship.rebuild_view()

    def on_damage_sound(self, *args):
        SoundManager().play_bullet_sound()

    def on_death_sound(self, *args):
        SoundManager().play_death_sound()

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
            self.toast.emit("Shoot")
            if self.entity.shoot():
                SoundManager().play_shoot_sound()
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

    def pick_up(self, item: Pickupable):
        super().pick_up(item)
        if isinstance(item, PickupableResource):
            self.score += item.resource.quantity

    @classmethod
    def from_dict(cls, data: Dict):
        defaults = super().get_default_params(data)
        defaults.pop("team")
        return cls(**defaults, score=data["score"])

    def to_dict(self) -> Dict:
        return {**super().to_dict(), "score": self.score}
