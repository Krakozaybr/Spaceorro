import math

from src.entities.abstract import Pilot, GuidedEntity
from src.controls import Controls
from src.entities.player.controls_config import *
from pymunk.vec2d import Vec2d
from src.settings import W, H


class PlayerPilot(Pilot):
    def __init__(self, entity: GuidedEntity):
        self.entity = entity

    def update(self, dt):
        controls = Controls.get_instance()

        up = controls.is_key_pressed(GO_UP)
        down = controls.is_key_pressed(GO_DOWN)
        left = controls.is_key_pressed(GO_LEFT)
        right = controls.is_key_pressed(GO_RIGHT)
        rotate_clockwise = controls.is_key_pressed(ROTATE_CLOCKWISE)
        rotate_counterclockwise = controls.is_key_pressed(ROTATE_COUNTERCLOCKWISE)
        rotate_to = controls.is_mouse_pressed(controls.LEFT_MOUSE_BTN)

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
            not (up or down),
            not (left or right),
            not (rotate_counterclockwise or rotate_clockwise or rotate_to),
        )
