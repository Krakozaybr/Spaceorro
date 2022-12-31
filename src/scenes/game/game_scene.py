from typing import Dict, Optional

import pygame
from pygame import Surface
from pymunk import Vec2d

from src.abstract import Serializable
from src.entities.entities_impls.player.entity import PlayerEntity
from src.map.impls.basic import BasicMap
from src.scenes.abstract import Scene
from .camera import Camera

from ...controls import Controls
from src.settings import load_game, save_game

from ...map.abstract import AbstractMap
from src.map.impls import map_from_dict
from src.entities import entity_from_dict


# TODO
class GameScene(Serializable, Scene):
    def __init__(
        self,
        camera: Optional[Camera] = None,
        player: Optional[PlayerEntity] = None,
        map_impl: Optional[AbstractMap] = None,
    ):
        self.camera = camera or Camera()
        self.player = player or PlayerEntity.create_default(Vec2d(0, 0))
        self.map = map_impl or BasicMap()
        self.player.add_to_space(self.map.space)

    def render(self, screen: Surface):
        self.map.render_at(screen, self.camera, self.player.position)
        self.player.render(screen, self.camera)

    def update(self, dt):
        self.camera.look_at(self.player)
        self.map.update_at(self.player.position, dt)
        self.player.update(dt)

        # Uncomment this to have opportunity to save game to game1.json by pressing key O
        # controls = Controls.get_instance()
        # if controls.is_key_pressed(pygame.K_o):  # Запомнить
        #     save_game("game1", self.serialize())

    # TODO serialization
    def to_dict(self) -> Dict:
        return {
            "class_name": self.__class__.__name__,
            "map": self.map.to_dict(),
            "player": self.player.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return GameScene(
            map_impl=map_from_dict(data["map"]), player=entity_from_dict(data["player"])
        )
