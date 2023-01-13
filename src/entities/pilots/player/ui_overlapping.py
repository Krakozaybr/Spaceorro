from typing import Dict, Tuple, Union

import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UITextBox

from src.abstract import Updateable
from src.resources import ResourceType, Resources
from src.settings import RESOURCE_LINE_HEIGHT, SHOW_FPS
from src.settings import W, H, FPS_UPDATE_TIME


class UIOverlapping(Updateable):
    resources: Resources
    manager: UIManager
    lines: Dict[ResourceType, UITextBox]
    current_toast: Tuple[str, float, Union[str, Tuple[int, int, int]]]
    font: pygame.font.Font

    MARGIN_LEFT = 10
    MARGIN_TOP = 10
    TOAST_DURATION = 2.3
    TOAST_DEFAULT_COLOR = (255, 255, 255)
    TOAST_MARGIN_BOTTOM = 20

    def __init__(self, resources: Resources, manager: UIManager):
        self.resources = resources
        self.manager = manager
        self.current_toast = "", 0, self.TOAST_DEFAULT_COLOR
        self.font = pygame.font.Font(None, 24)
        self.current_fps = 0
        self.fps_update_time = FPS_UPDATE_TIME
        self.cur_fps_update_time = 0

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

    def render(self, screen: pygame.Surface):
        # Resources
        for i, rt in enumerate(ResourceType):
            img = rt.get_image(RESOURCE_LINE_HEIGHT, RESOURCE_LINE_HEIGHT)
            screen.blit(img, (5, i * RESOURCE_LINE_HEIGHT + self.MARGIN_TOP))
        # Toast
        text, alpha, color = self.current_toast
        if alpha:
            rendered = self.font.render(text, False, color)
            rendered.set_alpha(int(255 * alpha))
            screen.blit(
                rendered,
                (
                    (W - rendered.get_width()) // 2,
                    (H - self.TOAST_MARGIN_BOTTOM - rendered.get_height()),
                ),
            )
        if SHOW_FPS:
            rendered = self.font.render(str(round(self.current_fps, 2)), False, "white")
            screen.blit(rendered, (W - rendered.get_width() - 10, 10))

    def update(self, dt: float):
        for i, rt in enumerate(ResourceType):
            resource = self.resources[rt]
            self.lines[rt].set_text(html_text=str(round(resource.quantity, 2)))
        text, alpha, color = self.current_toast
        self.current_toast = text, max(0.0, alpha - dt / self.TOAST_DURATION), color
        self.cur_fps_update_time += dt
        if self.cur_fps_update_time > self.fps_update_time:
            self.cur_fps_update_time = self.cur_fps_update_time % self.fps_update_time
            self.current_fps = 1 / dt

    def make_toast(
        self, text: str, color: Union[str, Tuple[int, int, int]] = TOAST_DEFAULT_COLOR
    ):
        self.current_toast = text, 1, color
