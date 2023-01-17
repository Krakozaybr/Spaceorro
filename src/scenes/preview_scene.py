import pygame
import pygame_gui
from pygame import Surface
from pygame_gui.elements import UITextBox

from .context import ContextScene, Context
from ..settings import PREVIEW_SCENE_THEME_PATH, W, H


class PreviewScene(ContextScene):
    def __init__(self, context: Context):
        super().__init__(context, theme_path=PREVIEW_SCENE_THEME_PATH)
        self.title = UITextBox(
            html_text="Spaceorro",
            manager=self.ui_manager,
            relative_rect=pygame.Rect(0, 0, W, H),
            anchors={"center": "center"},
        )
        self.title.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        self.animation_passed = False

    def render(self, screen: Surface):
        super().render(screen)

    def update(self, dt):
        super().update(dt)
        if self.animation_passed:
            self.context.launch_game_scene("game1")

    def process_event(self, e):
        super().process_event(e)
        if (
            e.type == pygame_gui.UI_TEXT_EFFECT_FINISHED
            and e.ui_element == self.title
            and e.effect == pygame_gui.TEXT_EFFECT_TYPING_APPEAR
        ):
            self.title.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT)
        if (
            e.type == pygame_gui.UI_TEXT_EFFECT_FINISHED
            and e.ui_element == self.title
            and e.effect == pygame_gui.TEXT_EFFECT_FADE_OUT
        ):
            self.animation_passed = True
