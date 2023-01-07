import math

import pymunk
from pymunk.vec2d import Vec2d

from src.entities.modifiers_and_characteristics import VelocityCharacteristics
from .abstract import Engine


class DefaultEngine(Engine):
    def __init__(
        self,
        body: pymunk.Body,
        control_body: pymunk.Body,
        characteristics: VelocityCharacteristics,
    ):
        self.body = body
        self.control_body = control_body
        self.characteristics = characteristics

    def rotate_clockwise(self, dt: float, power=1.0):
        self._rotate(dt * power)

    def update(self, dt: float):
        pass

    def rotate_counterclockwise(self, dt: float, power=1.0):
        self._rotate(-dt * power)

    def _rotate(self, k: float):
        self.body.angular_velocity += k * self.rotation_speed
        self.check_rotation()

    def rotate_to(self, dt: float, alpha: float):
        pi2 = math.pi * 2
        current_angle = self.body.angle % pi2
        k = -1
        if (current_angle - alpha) % pi2 > (alpha - current_angle) % pi2:
            k = 1
        dx = abs(current_angle - alpha)
        self.bring_rotate_speed_to(dt, self.rotation_speed * k * dx / math.pi)

    def move_to(self, dt: float, pos: Vec2d):
        vec, length = (pos - self.control_body.position).normalized_and_length()
        self.bring_speed_to(dt, vec * min(self.direct_force, length))

    def keep_distance(self, dt: float, pos: Vec2d, distance: float):
        vec = (self.control_body.position - pos).normalized()
        self.move_to(dt, vec * distance)

    def bring_speed_to(self, dt: float, speed: Vec2d):
        ds = self.direct_force * dt
        vel = self.control_body.velocity
        diff_vec, diff_length = (speed - vel).normalized_and_length()
        if diff_length <= ds:
            self.control_body.velocity = speed
        else:
            self.control_body.velocity += diff_vec * ds
        self.check_speed()

    def bring_rotate_speed_to(self, dt: float, speed: float):
        current_speed = self.body.angular_velocity
        force = self.rotation_speed * dt
        if abs(current_speed - speed) <= force:
            self.body.angular_velocity = speed
        elif current_speed - speed > 0:
            self.body.angular_velocity -= force
        else:
            self.body.angular_velocity += force
        self.check_rotation()

    def check_rotation(self):
        if self.body.angular_velocity < -self.max_rotation_speed:
            self.body.angular_velocity = -self.max_rotation_speed
        elif self.body.angular_velocity > self.max_rotation_speed:
            self.body.angular_velocity = self.max_rotation_speed

    def check_speed(self):
        normalized, length = self.control_body.velocity.normalized_and_length()
        if length > self.max_speed:
            self.control_body.velocity = normalized * self.max_speed

    def apply_force(self, force: Vec2d, dt: float):
        self.control_body.velocity += force.normalized() * self.direct_force * dt
        self.check_speed()

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
