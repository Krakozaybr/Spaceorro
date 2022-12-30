from typing import Dict

from pygame import Surface
from pymunk import Vec2d

from src.abstract import Serializable
from src.entities.entities_impls.player.entity import PlayerEntity
from src.map.impls.basic import BasicMap
from src.scenes.abstract import Scene
from .camera import Camera


# TODO
class GameScene(Serializable, Scene):
    def __init__(self):
        self.camera = Camera()
        self.player = PlayerEntity.create_default(Vec2d(0, 0))
        self.map = BasicMap()
        self.player.add_to_space(self.map.space)

    def render(self, screen: Surface):
        self.map.render_at(screen, self.camera, self.player.position)
        self.player.render(screen, self.camera)

    def update(self, dt):
        self.camera.look_at(self.player)
        self.map.update_at(self.player.position, dt)
        self.player.update(dt)

    # TODO serialization
    def to_dict(self) -> Dict:
        pass

    @classmethod
    def from_dict(cls, data: Dict):
        pass
