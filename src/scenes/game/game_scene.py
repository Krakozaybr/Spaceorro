from typing import Dict, Optional

import pygame
from pygame import Surface
from pymunk import Vec2d

from src.abstract import Serializable
from src.entities import entity_from_dict
from src.entities.spaceships.player.entity import PlayerEntity
from src.map.impls import map_from_dict
from src.map.impls.basic import BasicMap
from src.scenes.abstract import Scene
from .camera import Camera
from ...controls import Controls
from ...entities.abstract.abstract import Pilot, Entity
from ...environment.abstract import set_environment
from ...environment.impl import BasicEnvironment
from ...map.abstract import AbstractMap
from ...settings import save_game


class GameScene(Serializable, Scene):
    def __init__(
        self,
        camera: Optional[Camera] = None,
        player: Optional[PlayerEntity] = None,
        map_impl: Optional[AbstractMap] = None,
    ):
        Entity.store.clear()
        Pilot.store.clear()

        self.map = map_impl or BasicMap()
        environment = BasicEnvironment(self.map)
        set_environment(environment)

        self.camera = camera or Camera()
        self.player = player or PlayerEntity.create_default(Vec2d(0, 0))
        self.map.add_entity(self.player)

    def render(self, screen: Surface):
        self.map.render_at(screen, self.camera, self.player.position)

    def update(self, dt):
        self.camera.look_at(self.player)
        self.map.update_at(self.player.position, dt)

        if Controls().is_key_just_up(pygame.K_o):  # Запомнить
            save_game("game1", self.serialize())
            print("saved")

    def to_dict(self) -> Dict:
        return {
            "map": self.map.to_dict(),
            "player": self.player.to_dict(),
            **super().to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return GameScene(
            player=entity_from_dict(data["player"]), map_impl=map_from_dict(data["map"])
        )
