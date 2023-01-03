import pygame
from pygame import Surface
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.abstract import Updateable
from src.entities.abstract.abstract import Entity
from src.entities.basic_entity.view import BasicView
from src.entities.gadgets.health_bars.abstract import HealthBar
from src.entities.gadgets.health_bars.default_bars import NoHealthBar
from src.entities.gadgets.weapon.bullets import AbstractBullet
from src.settings import load_image
from src.utils.image_manager import ImageManager


class BlasterChargeView(BasicView, Updateable):
    animation_in_process: bool
    started_exposing: bool
    entity: AbstractBullet

    def __init__(self, entity: AbstractBullet, image: str, *groups: AbstractGroup):
        super().__init__(entity, *groups)

        # animation params
        self.started_exposing = False
        self.animation_in_process = False
        self.cur_image = 0
        self.time = 0
        self.fps = 10

        # default image
        self.image = self.apply_size(load_image(image))

    def apply_size(self, image: Surface, coef: float = 1.0) -> Surface:
        return pygame.transform.scale(image, (self.w * coef, self.h * coef))

    def start_exposing(self):
        self.started_exposing = True
        self.animation_in_process = True
        self.update_explosion_image()

    def init_sizes(self):
        r = self.entity.config.radius
        self.w = self.h = r * 2
        self.left_top_corner_delta = Vec2d(-r, -r)

    def draw_health_bar(self, screen: pygame.Surface, pos: Vec2d):
        pass

    @property
    def animation_passed(self):
        return self.started_exposing and not self.animation_in_process

    def create_health_bar(self) -> HealthBar:
        return NoHealthBar()

    def draw(self, screen: Surface, pos: Vec2d):
        x, y = pos
        screen.blit(
            self.image,
            (x - self.image.get_width() / 2, y - self.image.get_height() / 2),
        )

    def update(self, dt: float):
        if self.animation_in_process:
            explosion_frames = ImageManager().explosion_frames
            self.time += dt
            self.cur_image = int(self.time // (1 / self.fps))
            if self.cur_image >= len(explosion_frames):
                self.animation_in_process = False
            else:
                self.update_explosion_image()

    def update_explosion_image(self):
        img = ImageManager().explosion_frames[self.cur_image]
        r = self.entity.characteristics.explosion_radius
        self.image = pygame.transform.scale(img, (r * 2, r * 2))
