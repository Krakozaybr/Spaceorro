from src.scenes.abstract import Scene
from .camera import Camera
from src.entities.player.entity import PlayerEntity
from pymunk.vec2d import Vec2d
from src.abstract import Serializable
from src.map.impls.basic import BasicMap


# TODO
class GameScene(Serializable, Scene):
    def __init__(self):
        self.camera = Camera()
        self.player = PlayerEntity.create_default()
        self.map = BasicMap()
        self.player.add_to_space(self.map.space)

    def render(self, screen):
        self.map.render_at(screen, self.camera, self.player.position)
        self.player.render(screen, self.camera)

    def update(self, dt):
        self.camera.look_at(self.player)
        self.map.update_at(self.player.position, dt)
        self.player.update(dt)

    # TODO serialization
    def serialize(self):
        pass

    def deserialize(self, data):
        pass
