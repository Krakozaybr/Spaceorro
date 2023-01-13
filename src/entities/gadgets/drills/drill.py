import math
from typing import Dict, Optional, Union

import pygame.transform
from pygame import Surface
from pymunk import Vec2d

from src.entities.asteroids.abstract import AbstractAsteroid
from src.entities.basic_entity.basic_spaceship import SpaceshipMixin
from src.entities.gadgets.drills.abstract_drill import AbstractDrill
from src.entities.gadgets.drills.animation import DrillAnimation
from src.entities.gadgets.drills.config import DrillConfig
from src.entities.spaceships.miner.abstract_miner import AbstractMiner


class Drill(SpaceshipMixin[AbstractMiner], AbstractDrill):

    configs: Dict[int, DrillConfig]
    asteroid: Optional[AbstractAsteroid]
    animation: DrillAnimation

    def __init__(self, spaceship_id: int):
        super().__init__(spaceship_id)
        self.asteroid = None
        self.animation = DrillAnimation(self, 0)

    def can_mine(self, asteroid: AbstractAsteroid) -> bool:
        return (
            self.spaceship.position.get_distance(asteroid.position)
            <= self.config.mining_distance
        )

    def set_target(self, asteroid: Union[None, AbstractAsteroid]):
        self.asteroid = asteroid

    def render(self, screen: Surface, camera):
        if self.is_mining:
            src_img = self.animation.get_cur_image()
            angle = -(self.asteroid.position - self.spaceship.position).angle
            img = pygame.transform.rotate(src_img, angle / math.pi * 180)

            # vector to set the beginning of drill`s laser to the center of asteroid
            v = Vec2d(0, src_img.get_height() / 2).rotated(angle)
            vx, vy = abs(v.x), abs(v.y)
            if 0 <= angle <= math.pi / 2:  # need right top corner of img
                dx = -img.get_width() + vx
                dy = -vy
            elif math.pi / 2 <= angle <= math.pi:  # need left top corner of img
                dx = -vx
                dy = -vy
            elif 0 >= angle >= -math.pi / 2:  # need right bottom corner of img
                dx = -img.get_width() + vx
                dy = -img.get_height() + vy
            else:  # need left bottom corner of img
                dx = -vx
                dy = -img.get_height() + vy

            pos = self.asteroid.position + camera.dv + Vec2d(dx, dy)
            screen.blit(img, pos)
            # DEBUG
            # pygame.draw.rect(
            #     screen, "blue", (pos.x, pos.y, img.get_width(), img.get_height()), 2
            # )

    @property
    def is_mining(self) -> bool:
        return self.asteroid is not None and self.can_mine(self.asteroid)

    def update(self, dt: float):
        if self.is_mining:
            if not self.asteroid.is_alive:
                self.asteroid = None
            else:
                self.asteroid.mine(self.damage * dt)
                self.animation.set_width(
                    int(self.asteroid.position.get_distance(self.spaceship.position))
                )
                self.animation.update(dt)

    @property
    def config(self):
        return self.configs[self.spaceship.mining_characteristics.level]
