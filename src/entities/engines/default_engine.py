import math

import pymunk
from pymunk.vec2d import Vec2d

from src.entities.abstract import Engine
from math import inf


# TODO implement engine as it could influence on body of entity
class DefaultEngine(Engine):
    def __init__(
        self,
        body: pymunk.Body,
        control_body: pymunk.Body,
        max_speed=inf,
        max_rotation_speed=inf,
        stop_coef=1.0,
        stop_rotation_coef=0.1,
        direct_force=100,
        rotation_speed=100,
    ):
        self.rotation_speed = rotation_speed
        self.direct_force = direct_force
        self.body = body
        self.control_body = control_body
        self.max_speed = max_speed
        self.max_rotation_speed = max_rotation_speed
        self.stop_coef = stop_coef
        self.stop_rotation_coef = stop_rotation_coef

    def rotate_clockwise(self, dt: float):
        self.body.angular_velocity += dt * self.rotation_speed
        self.check_rotation()

    def rotate_counterclockwise(self, dt: float):
        self.body.angular_velocity -= dt * self.rotation_speed
        self.check_rotation()

    def check_rotation(self):
        if self.body.angular_velocity < -self.max_rotation_speed:
            self.body.angular_velocity = -self.max_rotation_speed
        elif self.body.angular_velocity > self.max_rotation_speed:
            self.body.angular_velocity = self.max_rotation_speed

    def apply_force(self, force: Vec2d, dt: float):
        self.control_body.velocity += force.normalized() * self.direct_force * dt
        normalized, length = self.control_body.velocity.normalized_and_length()
        if self.max_speed < length:
            self.control_body.velocity = self.max_speed * normalized

    def stop(self, dt: float, vertical=True, horizontal=True, rotation=True):
        vel = x, y = self.control_body.velocity
        direct_force = self.direct_force * dt * self.stop_coef
        if vertical and horizontal:
            if vel.length <= direct_force:
                self.control_body.velocity = Vec2d.zero()
            else:
                self.control_body.velocity -= vel.normalized() * direct_force
        elif vertical:
            if abs(y) <= direct_force:
                self.control_body.velocity = Vec2d(x, 0)
            else:
                self.control_body.velocity -= Vec2d(0, direct_force * y / abs(y))
        elif horizontal:
            if abs(x) <= direct_force:
                self.control_body.velocity = Vec2d(0, y)
            else:
                self.control_body.velocity -= Vec2d(direct_force * x / abs(x), 0)
        if rotation:
            rotation_force = self.rotation_speed * dt * self.stop_rotation_coef
            av = self.body.angular_velocity
            if rotation_force >= abs(self.body.angular_velocity):
                self.body.angular_velocity = 0
            else:
                self.body.angular_velocity -= rotation_force * av / abs(av)
