import math

from src.entities.abstract import Pilot, GuidedEntity
from src.controls import Controls
from src.entities.entities_impls.player.controls_config import *
from pymunk.vec2d import Vec2d
from src.settings import W, H


class PlayerPilot(Pilot):
    def __init__(self, entity: GuidedEntity):
        self.entity = entity
        # self.pos = Vec2d.zero()

    def update(self, dt: float):
        controls = Controls.get_instance()

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
