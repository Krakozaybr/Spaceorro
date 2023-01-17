import pygame
from pygame import Surface
from pygame_gui.elements import UITextBox, UIButton, UISelectionList

from .context import ContextScene, Context
from ..settings import MENU_SCENE_THEME_PATH


class MainMenuScene(ContextScene):

    LEFT_PADDING = 70
    TOP_PADDING = 150
    MENU_ITEM_SPACING = 30
    LEFT_BOXES_SIZE = 300, 50

    GAMES_MARGIN_LEFT = 70
    GAMES_WIDTH = 700
    GAMES_HEIGHT = 370

    def __init__(self, context: Context):
        super().__init__(context, theme_path=MENU_SCENE_THEME_PATH)
        self.title = UITextBox(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.TOP_PADDING, *self.LEFT_BOXES_SIZE
            ),
            object_id="#title_label",
            html_text="Spaceorro",
            manager=self.ui_manager,
        )
        self.new_game_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="New Game",
            anchors={"top_target": self.title},
        )
        self.load_game_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="Load Game",
            anchors={"top_target": self.new_game_btn},
        )
        self.game_controls_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="Controls",
            anchors={"top_target": self.load_game_btn},
        )
        self.exit_game_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="Exit game",
            anchors={"top_target": self.game_controls_btn},
        )

        self.games_title = UITextBox(
            relative_rect=pygame.Rect(
                self.GAMES_MARGIN_LEFT,
                self.TOP_PADDING,
                self.GAMES_WIDTH,
                self.LEFT_BOXES_SIZE[1],
            ),
            object_id="#games_title",
            html_text="Games",
            manager=self.ui_manager,
            anchors={"left_target": self.title},
        )
        self.games = UISelectionList(
            relative_rect=pygame.Rect(
                self.GAMES_MARGIN_LEFT,
                self.MENU_ITEM_SPACING,
                self.GAMES_WIDTH,
                self.GAMES_HEIGHT - self.games_title.get_starting_height(),
            ),
            manager=self.ui_manager,
            item_list=["12", "23"],
            anchors={'top_target': self.games_title, 'left_target': self.title}
        )

    def render(self, screen: Surface):
        super().render(screen)

    def update(self, dt):
        super().update(dt)
