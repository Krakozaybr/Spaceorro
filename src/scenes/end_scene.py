import pygame
from pygame import Surface
from pygame_gui.core import ObjectID
from pygame_gui.elements import UILabel, UIButton

from src.scenes.context import ContextScene, Context
from src.scenes.game.game_scene import GameScene
from src.settings import END_GAME_SCENE_THEME_PATH


class EndgameScene(ContextScene):

    TITLE_MARGIN_TOP = 100
    TITLE_SIZE = 600, 50
    SCORE_MARGIN_TOP = 20
    BTN_SIZE = 250, 70

    def __init__(self, context: Context, game_scene: GameScene):
        super().__init__(context, theme_path=END_GAME_SCENE_THEME_PATH)
        self.game_scene = game_scene
        self.title = UILabel(
            relative_rect=pygame.Rect(0, self.TITLE_MARGIN_TOP, *self.TITLE_SIZE),
            text="YOU DIED",
            object_id=ObjectID(object_id="#title", class_id=None),
            anchors={"centerx": "centerx"},
            manager=self.ui_manager,
        )
        self.score = UILabel(
            relative_rect=pygame.Rect(0, self.SCORE_MARGIN_TOP, *self.TITLE_SIZE),
            text=f"Score: {round(self.game_scene.player.score, 2)}",
            manager=self.ui_manager,
            anchors={"top_target": self.title, "centerx": "centerx"},
            object_id=ObjectID(object_id="#score", class_id=None),
        )
        self.main_menu_btn = UIButton(
            relative_rect=pygame.Rect(-self.BTN_SIZE[0] // 2, 0, *self.BTN_SIZE),
            text="Main menu",
            manager=self.ui_manager,
            anchors={"top_target": self.score, "centerx": "centerx"},
        )
        self.play_again_menu_btn = UIButton(
            relative_rect=pygame.Rect(0, 0, *self.BTN_SIZE),
            text="Load last save",
            manager=self.ui_manager,
            anchors={"top_target": self.score, "left_target": self.main_menu_btn},
        )

    def render(self, screen: Surface):
        super().render(screen)

    def update(self, dt: float):
        super().update(dt)
        if self.main_menu_btn.check_pressed():
            self.context.launch_main_menu_scene()
        elif self.play_again_menu_btn.check_pressed():
            self.context.launch_game_scene(self.game_scene.name)
