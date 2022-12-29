from abc import abstractmethod, ABC

import pymunk
from pymunk import Vec2d

from src.entities.characteristics import VelocityCharacteristics


class Engine(ABC):
    characteristics: VelocityCharacteristics
    body: pymunk.Body
    control_body: pymunk.Body

    @property
    def rotation_speed(self) -> float:
        return self.characteristics.rotation_speed

    @property
    def direct_force(self) -> float:
        return self.characteristics.direct_force

    @property
    def max_speed(self) -> float:
        return self.characteristics.max_speed

    @property
    def max_rotation_speed(self) -> float:
        return self.characteristics.max_rotation_speed

    @property
    def stop_coef(self) -> float:
        return self.characteristics.stop_coef

    @property
    def stop_rotation_coef(self) -> float:
        return self.characteristics.stop_rotation_coef

    @abstractmethod
    def stop(self, dt: float, vertical: bool, horizontal: bool, rotation: bool):
        pass

    @abstractmethod
    def rotate_clockwise(self, dt: float, power: float):
        pass

    @abstractmethod
    def rotate_counterclockwise(self, dt: float, power: float):
        pass

    @abstractmethod
    def rotate_to(self, dt: float, alpha: float):
        pass

    @abstractmethod
    def move_to(self, dt: float, pos: Vec2d):
        pass

    @abstractmethod
    def apply_force(self, force: Vec2d, dt: float):
        pass

    @abstractmethod
    def bring_rotate_speed_to(self, dt: float, speed: float):
        pass

    @abstractmethod
    def bring_speed_to(self, dt: float, speed: Vec2d):
        pass

    @abstractmethod
    def keep_distance(self, dt: float, pos: Vec2d, distance: float):
        pass
