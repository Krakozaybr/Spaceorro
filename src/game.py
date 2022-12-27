from src.scenes.game.game_scene import GameScene
import pygame
from settings import FPS, SIZE
from src.controls import Controls


class Game:
    def __init__(self):
        pygame.init()
        self.scene = GameScene()
        self.screen = pygame.display.set_mode(SIZE)

    def render(self):
        self.scene.render(self.screen)

    def update(self):
        self.scene.update(self.clock.get_time() / 1000)

    def catch_event(self, e):
        controls = Controls.get_instance()
        if e.type == pygame.QUIT:
            self.run = False
        if e.type == pygame.KEYDOWN:
            controls.set_key_pressed(e.key, True)
        if e.type == pygame.KEYUP:
            controls.set_key_pressed(e.key, False)

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
