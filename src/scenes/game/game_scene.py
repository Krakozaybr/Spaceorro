from typing import Dict, Optional

import pygame
from pygame import Surface
from pymunk import Vec2d

from src.abstract import Serializable
from src.entities.get_entity import entity_from_dict
from src.entities.spaceships.player.entity import PallariansCruiser
from src.map.impls import map_from_dict
from src.map.impls.basic import BasicMap
from src.scenes.abstract import Scene
from .camera import Camera
from ...controls import Controls
from ...entities.basic_entity.basic_spaceship import BasicSpaceship
from ...entities.pilots.player.player import PlayerPilot
from ...environment.abstract import set_environment
from ...environment.impl import BasicEnvironment
from ...map.abstract import AbstractMap
from ...settings import save_game


class GameScene(Serializable, Scene):
    def __init__(
        self,
        camera: Optional[Camera] = None,
        player: Optional[PlayerPilot] = None,
        player_entity: Optional[BasicSpaceship] = None,
        map_impl: Optional[AbstractMap] = None,
    ):
        super().__init__()

        self.map = map_impl or BasicMap()
        environment = BasicEnvironment(self.map)
        set_environment(environment)

        self.camera = camera or Camera()

        self.player = player or PlayerPilot(
            spaceship=player_entity, manager=self.ui_manager
        )
        self.player_entity = player_entity or PallariansCruiser.create_default(
            Vec2d(0, 0)
        )
        if player_entity is None or player is not None:
            self.player.set_spaceship(self.player_entity)
        if player is not None:
            self.player.set_manager(self.ui_manager)

        self.map.add_entity(self.player_entity)

    def render(self, screen: Surface):
        self.map.render_at(screen, self.camera, self.player_entity.position)
        self.player.render(screen)
        super().render(screen)

    def update(self, dt):
        super().update(dt)
        self.camera.look_at(self.player_entity)
        self.map.update_at(self.player_entity.position, dt)

        if Controls().is_key_just_up(pygame.K_o):  # Запомнить
            save_game("game1", self.serialize())
            print("saved")

    def to_dict(self) -> Dict:
        self.map.remove_entity(self.player_entity)
        res = {
            "map": self.map.to_dict(),
            "player": self.player_entity.to_dict(),
            **super().to_dict(),
        }
        self.map.add_entity(self.player_entity)
        return res

    @classmethod
    def from_dict(cls, data: Dict):
        entity = entity_from_dict(data["player"])
        player = entity.pilot
        return GameScene(
            player_entity=entity, player=player, map_impl=map_from_dict(data["map"])
        )
