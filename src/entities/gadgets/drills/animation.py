from typing import List

import pygame.transform
from pygame import Surface
from pymunk import Vec2d

from src.abstract import Updateable
from src.entities.gadgets.drills.abstract_drill import AbstractDrill
from src.entities.gadgets.drills.config import DrillConfig
from src.settings import FPS
from src.utils.image_manager import ImageManager


class DrillAnimation(Updateable):

    drill: AbstractDrill
    w: int
    cur_image: int
    _images: List[Surface]

    def __init__(self, drill: AbstractDrill, w: int):
        self.drill = drill
        self.cur_image = self.cur_time = 0
        self.time = 1 / FPS
        self.w = w
        self.changed = True

    @property
    def images(self):
        if self.changed:
            self._images = [
                pygame.transform.scale(
                    i, (i.get_width(), self.drill.config.animation_height)
                )
                for i in ImageManager().get_crop_gif(
                    self.drill.config.gif, -self.w, 0, self.w, 0
                )
            ]
        return self._images.copy()

    def set_width(self, w: int):
        if w != self.w:
            self.changed = True
            self.w = w

    def get_cur_image(self):
        return self.images[self.cur_image]

    def update(self, dt: float):
        self.cur_time += dt
        self.cur_image = (self.cur_image + int(self.cur_time / self.time)) % len(
            self.images
        )
        self.cur_time = self.cur_time % self.time
