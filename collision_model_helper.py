import os.path

import pygame
from PIL import Image
from pygame import Surface

from src.controls import Controls
from src.game import Game
from src.scenes.context import ContextScene
from src.settings import IMAGES_DIR, SIZE, CONFIGS_DIR

name = "traders trader.png"
path = os.path.join(IMAGES_DIR, name)


class HelperScene(ContextScene):
    def __init__(self, context, src: str):
        super().__init__(context)
        img = Image.open(src)
        self.src = src
        self.pixels = img.load()
        self.w, self.h = img.size
        self.colors = [self.pixels[i, j] for i in range(self.w) for j in range(self.h)]
        self.points = []
        self.weapon_pos = (0, 0)
        self.dx = self.dy = 0
        self._s = 100
        self._size = 2
        self.scale = 1

    @property
    def size(self):
        return self._size * self.scale

    @property
    def s(self):
        return self.scale * self._s

    def render(self, screen: Surface):
        for i in range(self.w):
            for j in range(self.h):
                pygame.draw.rect(screen, self.pixels[i, j], self.get_rect(i, j))
        for x, y in self.points:
            pygame.draw.rect(screen, (255, 0, 0), self.get_rect(x, y))
        if len(self.points) >= 2:
            pygame.draw.lines(
                screen,
                "red",
                True,
                [(self.apply_x(x), self.apply_y(y)) for x, y in self.points],
            )
        if self.weapon_pos:
            x, y = self.weapon_pos
            pygame.draw.rect(screen, "yellow", self.get_rect(x, y))

    def apply_x(self, x):
        return x * self.size + self.dx

    def apply_y(self, y):
        return y * self.size + self.dy

    def get_rect(self, x, y):
        return pygame.Rect(
            self.apply_x(x),
            self.apply_y(y),
            self.size,
            self.size,
        )

    def update(self, dt: float):
        controls = Controls()
        if controls.is_mouse_just_down(controls.MIDDLE_MOUSE_BTN_DOWN):
            self.scale *= 1.1
            self.dx *= 1.1
            self.dy *= 1.1
        if controls.is_mouse_just_down(controls.MIDDLE_MOUSE_BTN_UP):
            self.scale /= 1.1
            self.dx /= 1.1
            self.dy /= 1.1

        if controls.is_key_pressed(pygame.K_LEFT):
            self.dx += self.s * dt
        if controls.is_key_pressed(pygame.K_RIGHT):
            self.dx -= self.s * dt
        if controls.is_key_pressed(pygame.K_UP):
            self.dy += self.s * dt
        if controls.is_key_pressed(pygame.K_DOWN):
            self.dy -= self.s * dt

        if controls.is_mouse_just_down(controls.LEFT_MOUSE_BTN):
            x, y = controls.get_mouse_pos()
            self.points.append(
                (
                    int((x - self.dx) // self.size),
                    int((y - self.dy) // self.size),
                )
            )
        elif controls.is_mouse_just_down(controls.RIGHT_MOUSE_BTN):
            x, y = controls.get_mouse_pos()
            self.weapon_pos = (
                int((x - self.dx) // self.size),
                int((y - self.dy) // self.size),
            )
        if (
            controls.is_key_pressed(pygame.K_LCTRL)
            and controls.is_key_just_down(pygame.K_z)
            and self.points
        ):
            self.points.pop()

        if controls.is_key_just_down(pygame.K_p):
            global name
            file = os.path.join(os.path.join(CONFIGS_DIR, 'spaceships/general'), name.replace('.png', '.json').replace(' ', '_'))
            with open(file, 'w') as f:
                print("{", file=f)
                print('  "mass": 5000,', file=f)
                print(
                    f'  "vertices": {[[x - self.w // 2, y - self.h // 2] for x, y in self.points]},', file=f
                )
                print(
                    f'  "blaster_relative_position": {[self.weapon_pos[0] - self.w // 2, self.weapon_pos[1] - self.h // 2]}', file=f
                )
                print("}", file=f)


class SubGame(Game):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.scene = HelperScene(self, path)
        self.screen = pygame.display.set_mode(SIZE)


game = SubGame()
game.start()
