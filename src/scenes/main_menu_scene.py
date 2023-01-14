from pygame import Surface

from .abstract import Scene
from .context import ContextScene, Context


# TODO implement that
class MainMenuScene(ContextScene):
    def __init__(self, context: Context):
        super().__init__(context)

    def render(self, screen: Surface):
        super().render(screen)

    def update(self, dt):
        super().update(dt)
