from typing import Optional

import pygame
from pygame import Surface
from pymunk import Vec2d

from src.abstract import Serializable
from src.entities.get_entity import *
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
from ...settings import GAME_SCENE_THEME_PATH


class GameScene(Serializable, ContextScene):

    _pause: bool
    name: str
    ui: UIOverlapping

    def __init__(
        self,
        name: str,
        context: Context,
        camera: Optional[Camera] = None,
        player: Optional[PlayerPilot] = None,
        player_entity: Optional[BasicSpaceship] = None,
        map_impl: Optional[AbstractMap] = None,
    ):
        ContextScene.__init__(self, context, theme_path=GAME_SCENE_THEME_PATH)

        # Settings
        self._pause = False
        self.name = name

        # Map and environment
        self.map = map_impl or BasicMap()
        environment = BasicEnvironment(self.map)
        set_environment(environment)

        # Camera
        self.camera = camera or Camera()

        # Player pilot and its spaceship
        self.player = player or PlayerPilot(entity=player_entity)
        self.player_entity = player_entity or AliensDrone(
            Vec2d(0, 0), pilot=self.player
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

        if Controls().is_key_just_down(pygame.K_ESCAPE):
            self.context.launch_game_menu_scene(self)

        if not self.player.entity.is_active:
            self.context.launch_game_end_scene(self)

    def to_dict(self) -> Dict:
        self.map.remove_entity(self.player_entity)
        res = {
            "name": self.name,
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
            name=data["name"],
            context=data["context"],
            player_entity=entity,
            player=player,
            map_impl=map_from_dict(data["map"]),
        )
