from src.scenes.abstract import Scene
from .camera import Camera
from src.entities.player.pilot import PlayerPilot
from src.utils.vector import Vector


# TODO
class GameScene(Scene):

    def __init__(self):
        self.camera = Camera()
        self.player = PlayerPilot(Vector(0, 0))

    def render(self, screen):
        ...

    def update(self, dt):
        ...

    def catch_event(self, e):
        ...

    # TODO serialization
    # def serialize(self):
    #     pass
    #
    # def deserialize(self, data):
    #     pass
