from src.scenes.abstract import Scene
from .camera import Camera
from src.entities.player.pilot import PlayerPilot
from pymunk.vec2d import Vec2d
from src.abstract import Serializable
from src.map.impls.basic import BasicMap


# TODO
class GameScene(Serializable, Scene):
    def __init__(self):
        self.camera = Camera()
        self.player = PlayerPilot(Vec2d(0, 0))
        self.map = BasicMap()
        self.player.entity.add_to_space(self.map.space)

    def render(self, screen):
        self.map.render_at(screen, self.camera, self.player.entity.position)
        self.player.render(screen, self.camera)

    def update(self, dt):
        self.camera.look_at(self.player.entity)
        self.map.update_at(self.player.entity.position, dt)
        self.player.update(dt)

    # TODO serialization
    def serialize(self):
        pass

    def deserialize(self, data):
        pass
