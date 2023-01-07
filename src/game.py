from src.scenes.game.game_scene import GameScene
import pygame
from settings import FPS, SIZE
from src.controls import Controls
from pymunk import Vec2d
from src.settings import load_game, SAVE_GAME
import sys
from pygame.locals import *
from game_object import GameObject


class Game:
    def __init__(self):
        pygame.init()
        if SAVE_GAME:
            self.scene = GameScene.deserialize(load_game("Infinity War", "",
                                                         "Главная цель игры - выжить как можно дольше",
                                                         "Уворачвайся от метеоритов, собирай бонусы."))
        else:
            self.scene = GameScene()
        self.screen = pygame.display.set_mode(SIZE)

    def render(self):
        self.scene.render(self.screen)

    def update(self):
        dt = self.clock.get_time() / 1000
        self.scene.update(dt)
        Controls().update()

    def catch_event(self, e):
        controls = Controls()
        if e.type == pygame.QUIT:
            self.run = False
        if e.type == pygame.KEYDOWN:
            controls.set_key_pressed(e.key, True)
        if e.type == pygame.KEYUP:
            controls.set_key_pressed(e.key, False)
        if e.type == pygame.MOUSEBUTTONDOWN:
            controls.set_mouse_pressed(e.button, True)
        if e.type == pygame.MOUSEBUTTONUP:
            controls.set_mouse_pressed(e.button, False)
        if e.type == pygame.MOUSEMOTION:
            x, y = e.pos
            controls.set_mouse_pos(Vec2d(x, y))

    def start(self):
        self.clock = pygame.time.Clock()
        self.run = True
        while self.run:
            for event in pygame.event.get():
                self.catch_event(event)
            self.screen.fill((0, 0, 0))
            self.update()
            self.render()
            self.clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()


class TextObject:
    def __init__(self,
                 x,
                 y,
                 text_func,
                 color,
                 font_name,
                 font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = \
            self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2,
                   self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text,
                                        False,
                                        self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass


class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)