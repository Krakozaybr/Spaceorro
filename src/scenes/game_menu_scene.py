from .abstract import Scene
from pygame import Surface

from .context import ContextScene, Context


# TODO implement that
class GameMenuScene(ContextScene):
    def __init__(self, context: Context, game_scene: Scene):
        super().__init__(context)
        self.game_scene = game_scene
        self.background = context.screenshot()

    def render(self, screen: Surface):
        super().render(screen)

    def update(self, dt):
        super().update(dt)
