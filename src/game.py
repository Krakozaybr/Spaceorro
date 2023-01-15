from typing import Type

import pygame
import pygame_gui
from pymunk import Vec2d

from src.scenes.abstract import Scene
from src.scenes.context import Context
from src.scenes.game_menu_scene import GameMenuScene
from src.scenes.main_menu_scene import MainMenuScene
from src.settings import FPS, SIZE
from src.controls import Controls
from src.scenes.game.game_scene import GameScene
from src.settings import load_game, SAVE_GAME


class Game(Context):
    def __init__(self):
        pygame.init()
        if SAVE_GAME:
            self.launch_game_scene("game1")
        else:
            self.scene = GameScene(self)
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
        if e.type == pygame_gui.UI_BUTTON_PRESSED:
            controls.set_button_pressed(e.ui_element)
        self.scene.process_event(e)

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

    def change_scene(self, sender: Scene, target: Type[Scene], **kwargs):
        self.scene = target(context=self, **kwargs)

    def launch_main_menu_scene(self):
        self.scene = MainMenuScene(self)

    def launch_game_scene(self, save_name: str):
        data = load_game(save_name)
        data["context"] = self
        self.scene = GameScene.from_dict(data)

    def launch_game_menu_scene(self, game_scene: Scene):
        self.scene = GameMenuScene(self, game_scene)

    def screenshot(self) -> pygame.Surface:
        return self.screen.copy()
