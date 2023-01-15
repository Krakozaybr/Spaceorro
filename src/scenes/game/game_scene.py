from typing import Dict, Optional

import pygame
from pygame import Surface
from pymunk import Vec2d

from src.abstract import Serializable
from src.entities.get_entity import entity_from_dict
from src.entities.spaceships.pallarians import PallariansCruiser
from src.map.impls import map_from_dict
from src.map.impls.basic import BasicMap
from .camera import Camera
from .ui_overlapping import UIOverlapping
from ..context import ContextScene, Context
from ...controls import Controls
from ...entities.basic_entity.basic_spaceship import BasicSpaceship
from ...entities.pilots.player.player import PlayerPilot
from ...environment.abstract import set_environment
from ...environment.impl import BasicEnvironment
from ...map.abstract import AbstractMap
from ...settings import save_game


class GameScene(Serializable, ContextScene):

    _pause: bool
    ui = UIOverlapping

    def __init__(
        self,
        context: Context,
        camera: Optional[Camera] = None,
        player: Optional[PlayerPilot] = None,
        player_entity: Optional[BasicSpaceship] = None,
        map_impl: Optional[AbstractMap] = None,
    ):
        ContextScene.__init__(self, context)

        # Settings
        self._pause = False

        # Map and environment
        self.map = map_impl or BasicMap()
        environment = BasicEnvironment(self.map)
        set_environment(environment)

        # Camera
        self.camera = camera or Camera()

        # Player pilot and its spaceship
        self.player = player or PlayerPilot(entity=player_entity)
        self.player_entity = player_entity or PallariansCruiser.create_default(
            Vec2d(0, 0)
        )
        if player_entity is None or player is not None:
            self.player.set_spaceship(self.player_entity)
        self.map.add_entity(self.player_entity)

        # UI
        self.ui = UIOverlapping(target=self.player, manager=self.ui_manager)

    @property
    def pause(self) -> bool:
        return self._pause

    @pause.setter
    def pause(self, val: bool):
        self._pause = val
        self.ui.paused = val

    def render(self, screen: Surface):
        self.map.render_at(screen, self.camera, self.player_entity.position)
        self.ui.render(screen)
        super().render(screen)

    def update(self, dt):
        super().update(dt)
        self.camera.look_at(self.player_entity)
        if not self.pause:
            self.map.update_at(self.player_entity.position, dt)
        self.ui.update(dt)

        if Controls().is_key_just_up(pygame.K_p):
            self.pause = not self.pause

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
            context=data["context"],
            player_entity=entity,
            player=player,
            map_impl=map_from_dict(data["map"]),
        )
