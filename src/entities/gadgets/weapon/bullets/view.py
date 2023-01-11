import pygame
from pygame import Surface
from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.basic_entity.explosive import ExplosiveView
from src.entities.gadgets.weapon.bullets.abstract import AbstractBullet
from src.settings import load_image


class BlasterChargeView(ExplosiveView):
    animation_in_process: bool
    started_exposing: bool
    entity: AbstractBullet

    def __init__(self, entity: AbstractBullet, image: str, *groups: AbstractGroup):
        super().__init__(entity, entity.characteristics.explosion_radius, *groups)
        # default image
        self.image = self.apply_size(load_image(image))

    def apply_size(self, image: Surface, coef: float = 1.0) -> Surface:
        return pygame.transform.scale(image, (int(self.w * coef), int(self.h * coef)))

    def init_sizes(self):
        r = self.entity.config.radius
        self.w = self.h = r * 2
        self.right_top_corner_delta = Vec2d(-r, -r)

    def draw_image(self, screen: pygame.Surface, pos: Vec2d) -> None:
        x, y = pos
        screen.blit(
            self.image,
            (x - self.image.get_width() / 2, y - self.image.get_height() / 2),
        )
