import pygame
from pygame import Surface

from .abstract import Scene

# from game_object import GameObject
from .context import ContextScene, Context


class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass


# class Paddle(GameObject):
#     def __init__(self, x, y, w, h, color, offset):
#         GameObject.__init__(self, x, y, w, h)
#         self.color = color
#         self.offset = offset
#         self.moving_left = False
#         self.moving_right = False
#
#     def draw(self, surface):
#         pygame.draw.rect(surface, self.color, self.bounds)


# TODO implement that
class PreviewScene(ContextScene):
    def __init__(self, context: Context):
        super().__init__(context)

    def render(self, screen: Surface):
        super().render(screen)

    def update(self, dt):
        super().update(dt)
