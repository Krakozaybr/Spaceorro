import math
from typing import Dict, Optional

from pygame import Surface
from pygame_gui import UIManager
from pymunk.vec2d import Vec2d

from src.controls import Controls
from src.entities.basic_entity.basic_spaceship import BasicSpaceship
from src.entities.pilots.basic_pilot import BasicPilot
from src.entities.pilots.controls_config import *
from src.entities.pilots.player.ui_overlapping import UIOverlapping
from src.entities.teams import Team
from src.resources import Resources
from src.settings import W, H


class PlayerPilot(BasicPilot):

    entity: BasicSpaceship
    ui: Optional[UIOverlapping]

    def __init__(
        self,
        entity: Optional[BasicSpaceship] = None,
        manager: Optional[UIManager] = None,
        _id: Optional[int] = None,
        resources: Optional[Resources] = None,
    ):
        super().__init__(
            entity=entity, _id=_id, resources=resources, team=Team.player
        )
        self.ui = None
        if manager is not None:
            self.ui = UIOverlapping(manager=manager, resources=self.resources)

    def set_manager(self, manager: UIManager):
        self.ui = UIOverlapping(manager=manager, resources=self.resources)

    def set_spaceship(self, spaceship: BasicSpaceship):
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
        rotate_to = controls.is_mouse_pressed(controls.LEFT_MOUSE_BTN)
        # move_to = controls.is_key_pressed(pygame.K_h)

        # if controls.is_key_pressed(pygame.K_t):
        #     self.pos = controls.mouse_pos - Vec2d(W / 2, H / 2) + self.entity.position
        #     print(self.pos)
        # if move_to:
        #     self.entity.engine.move_to(dt, self.pos)

        if self.ui is not None and controls.is_key_pressed(pygame.K_t):
            self.ui.make_toast("lolll")

        if controls.is_key_pressed(FIRE):
            self.entity.shoot()
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
        if rotate_to:
            angle = (controls.get_mouse_pos() - Vec2d(W / 2, H / 2)).angle
            self.entity.engine.rotate_to(dt, (angle + math.pi / 2) % (math.pi * 2))
        self.entity.engine.stop(
            dt,
            not (up or down),  # not (up or down or move_to),
            not (left or right),  # not (left or right or move_to),
            not (rotate_counterclockwise or rotate_clockwise or rotate_to),
        )

        if self.ui is not None:
            self.ui.update(dt)

    def render(self, screen: Surface):
        if self.ui is not None:
            self.ui.render(screen)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**super().get_default_params(data))
