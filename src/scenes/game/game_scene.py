from typing import Dict, Optional

import pygame
from pygame import Surface
from pygame_gui import UIManager
from pygame_gui.elements import UITextBox
from pymunk import Vec2d

from src.abstract import Serializable, RenderUpdateObject, Updateable
from src.entities.get_entity import entity_from_dict
from src.entities.spaceships.player.entity import PlayerEntity
from src.map.impls import map_from_dict
from src.map.impls.basic import BasicMap
from src.scenes.abstract import Scene
from .camera import Camera
from ...controls import Controls
from ...entities.abstract.abstract import Entity
from src.entities.pilots.abstract import Pilot
from ...entities.pilots.player import Pilot
from ...environment.abstract import set_environment
from ...environment.impl import BasicEnvironment
from ...map.abstract import AbstractMap
from ...resources import Resources, ResourceType
from ...settings import save_game, RESOURCE_LINE_HEIGHT


class UIOverlapping(Updateable):
    pilot: Pilot
    resources: Resources
    manager: UIManager
    lines: Dict[ResourceType, UITextBox]

    MARGIN_LEFT = 10
    MARGIN_TOP = 10

    def __init__(self, pilot: Pilot, manager: UIManager):
        self.pilot = pilot
        self.resources = pilot.resources
        self.manager = manager

        self.lines = {
            rt: UITextBox(
                html_text="0",
                relative_rect=pygame.Rect(
                    RESOURCE_LINE_HEIGHT + self.MARGIN_LEFT,
                    i * RESOURCE_LINE_HEIGHT + self.MARGIN_TOP,
                    70,
                    RESOURCE_LINE_HEIGHT,
                ),
                manager=manager,
            )
            for i, rt in enumerate(ResourceType)
        }

    def render(self, screen: Surface):
        for i, rt in enumerate(ResourceType):
            img = rt.get_image(RESOURCE_LINE_HEIGHT, RESOURCE_LINE_HEIGHT)
            screen.blit(img, (5, i * RESOURCE_LINE_HEIGHT + self.MARGIN_TOP))

    def update(self, dt: float):
        for i, rt in enumerate(ResourceType):
            resource = self.resources[rt]
            self.lines[rt].set_text(html_text=str(round(resource.quantity, 2)))


class GameScene(Serializable, Scene):
    def __init__(
        self,
        camera: Optional[Camera] = None,
        player: Optional[PlayerEntity] = None,
        map_impl: Optional[AbstractMap] = None,
    ):
        super().__init__()

        self.map = map_impl or BasicMap()
        environment = BasicEnvironment(self.map)
        set_environment(environment)

        self.camera = camera or Camera()
        self.player = player or PlayerEntity.create_default(Vec2d(0, 0))
        self.map.add_entity(self.player)
        self.ui = UIOverlapping(self.player.pilot, self.ui_manager)

    def render(self, screen: Surface):
        self.map.render_at(screen, self.camera, self.player.position)
        self.ui.render(screen)
        super().render(screen)

    def update(self, dt):
        super().update(dt)
        self.camera.look_at(self.player)
        self.map.update_at(self.player.position, dt)
        self.ui.update(dt)

        if Controls().is_key_just_up(pygame.K_o):  # Запомнить
            save_game("game1", self.serialize())
            print("saved")

    def to_dict(self) -> Dict:
        self.map.remove_entity(self.player)
        res = {
            "map": self.map.to_dict(),
            "player": self.player.to_dict(),
            **super().to_dict(),
        }
        self.map.add_entity(self.player)
        return res

    @classmethod
    def from_dict(cls, data: Dict):
        return GameScene(
            player=entity_from_dict(data["player"]), map_impl=map_from_dict(data["map"])
        )
