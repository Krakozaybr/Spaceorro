from typing import Dict, Tuple, Union

import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UITextBox, UIButton

from src.abstract import Updateable
from src.entities.basic_entity.mixins.upgradeable_spaceship_mixin import (
    UpgradeableSpaceshipMixin,
)
from src.entities.pilots.basic_pilot import BasicPilot
from src.resources import ResourceType
from src.scenes.game.upgrades_window import UpgradesWindow
from src.settings import RESOURCE_LINE_HEIGHT, SHOW_FPS, UPGRADES_BTN_HEIGHT
from src.settings import W, H, FPS_UPDATE_TIME
from src.utils.timer import Timer


class UIOverlapping(Updateable):
    target: BasicPilot
    manager: UIManager
    lines: Dict[ResourceType, UITextBox]
    current_toast: Tuple[str, float, Union[str, Tuple[int, int, int]]]
    fps_font: pygame.font.Font
    paused: bool
    last_fps: float

    MARGIN_LEFT = 10
    MARGIN_TOP = 10
    TOAST_DURATION = 2.3
    TOAST_DEFAULT_COLOR = (255, 255, 255)
    TOAST_MARGIN_BOTTOM = 20

    def __init__(
        self,
        target: BasicPilot,
        manager: UIManager,
    ):
        self.target = target
        self.target.toast.connect(self.make_toast)

        self.manager = manager
        self.current_toast = "", 0, self.TOAST_DEFAULT_COLOR

        self.fps_timer = Timer(FPS_UPDATE_TIME, self.update_fps)
        self.current_fps = 0
        self.fps_font = pygame.font.Font(None, 24)

        self.paused_font = pygame.font.Font(None, 36)
        self.paused = False

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

        # Upgrade system
        if isinstance(self.target.entity, UpgradeableSpaceshipMixin):
            self.upgrades_button = UIButton(
                relative_rect=pygame.Rect(
                    self.MARGIN_LEFT,
                    H - UPGRADES_BTN_HEIGHT - 10,
                    100,
                    UPGRADES_BTN_HEIGHT,
                ),
                text="Upgrades",
                manager=manager,
                tool_tip_text="Upgrades for your spaceship",
            )
        self.cur_window = None

    def update_target(self, target: BasicPilot):
        self.target.toast.remove(self.make_toast)
        self.target = target
        self.target.toast.connect(self.make_toast)

    def update_fps(self):
        self.current_fps = self.last_fps

    def render(self, screen: pygame.Surface):
        # Resources
        for i, rt in enumerate(ResourceType):
            img = rt.get_image(RESOURCE_LINE_HEIGHT, RESOURCE_LINE_HEIGHT)
            screen.blit(img, (5, i * RESOURCE_LINE_HEIGHT + self.MARGIN_TOP))

        # Toast
        text, alpha, color = self.current_toast
        if alpha:
            rendered = self.fps_font.render(text, False, color)
            rendered.set_alpha(int(255 * alpha))
            screen.blit(
                rendered,
                (
                    (W - rendered.get_width()) // 2,
                    (H - self.TOAST_MARGIN_BOTTOM - rendered.get_height()),
                ),
            )

        # FPS
        if SHOW_FPS:
            rendered = self.fps_font.render(
                str(round(self.current_fps, 2)), False, "white"
            )
            screen.blit(rendered, (W - rendered.get_width() - 10, 10))

        # Paused
        if self.paused:
            rendered = self.paused_font.render("Pause", False, "white")
            screen.blit(rendered, ((W - rendered.get_width()) // 2, 10))

    def update(self, dt: float):
        # Resources
        for i, rt in enumerate(ResourceType):
            resource = self.target.resources[rt]
            self.lines[rt].set_text(html_text=str(round(resource.quantity, 2)))

        # Toast
        text, alpha, color = self.current_toast
        self.current_toast = text, max(0.0, alpha - dt / self.TOAST_DURATION), color

        # FPS
        self.last_fps = 0 if not dt else 1 / dt
        self.fps_timer.update(dt)

        # Upgrades
        if hasattr(self, "upgrades_button") and self.upgrades_button.check_pressed():
            if self.cur_window is not None:
                self.cur_window.on_close_window_button_pressed()
            self.cur_window = UpgradesWindow(
                manager=self.manager, upgrade_system=self.target.entity.upgrade_system
            )

    def make_toast(
        self, text: str, color: Union[str, Tuple[int, int, int]] = TOAST_DEFAULT_COLOR
    ):
        self.current_toast = text, 1, color
