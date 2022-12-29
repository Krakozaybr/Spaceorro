from pygame import Surface

from .abstract import Scene


# TODO implement that
class PreviewScene(Scene):
    def render(self, screen: Surface):
        ...

    def update(self, dt):
        ...
