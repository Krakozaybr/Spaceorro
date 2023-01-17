import pygame
import pygame_gui
from pygame import Surface
from pygame_gui import UIManager
from pygame_gui.core import ObjectID
from pygame_gui.windows import UIMessageWindow, UIConfirmationDialog
from pygame_gui.elements import (
    UITextBox,
    UIButton,
    UISelectionList,
    UITextEntryLine,
    UIWindow,
)

from src.settings import W, H, delete_game
from .context import ContextScene, Context
from ..settings import MENU_SCENE_THEME_PATH, get_saves
from ..utils.signal import SignalFieldMixin, Signal


class GetSaveNameDialog(UIWindow, SignalFieldMixin):

    WIDTH, HEIGHT = 300, 140
    SIZE = ((H - HEIGHT) // 2, (W - WIDTH) // 2, WIDTH, HEIGHT)
    INPUT_SIZE = 267, 40
    BUTTON_SIZE = 90, 30
    BUTTON_TOP_MARGIN = 10

    cancel = Signal()
    accept = Signal()

    def __init__(self, manager: UIManager):
        SignalFieldMixin.__init__(self)
        UIWindow.__init__(
            self,
            rect=pygame.Rect(*self.SIZE),
            manager=manager,
            window_display_title="Save name",
        )
        self.input = UITextEntryLine(
            relative_rect=pygame.Rect(0, 0, *self.INPUT_SIZE),
            manager=manager,
            container=self,
            placeholder_text="Save name",
            anchors={"top": "top"},
        )
        self.accept_btn = UIButton(
            relative_rect=pygame.Rect(0, self.BUTTON_TOP_MARGIN, *self.BUTTON_SIZE),
            text="Ok",
            manager=manager,
            container=self,
            object_id=ObjectID(object_id="#dialog_accept_btn", class_id="@dialog_btn"),
            anchors={"left": "left", "top_target": self.input},
        )
        self.cancel_btn = UIButton(
            relative_rect=pygame.Rect(0, self.BUTTON_TOP_MARGIN, *self.BUTTON_SIZE),
            text="Cancel",
            manager=manager,
            container=self,
            object_id=ObjectID(object_id="#dialog_cancel_btn", class_id="@dialog_btn"),
            anchors={"left_target": self.accept_btn, "top_target": self.input},
        )
        self.accept.connect(self.on_close_window_button_pressed)
        self.cancel.connect(self.on_close_window_button_pressed)

    def update(self, time_delta: float):
        super().update(time_delta)
        if self.accept_btn.check_pressed():
            self.accept.emit()
        if self.cancel_btn.check_pressed():
            self.cancel.emit()

    def get_text(self) -> str:
        return self.input.get_text()


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

        self.saves = dict()  # list_name: save_name

        self.title = UITextBox(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.TOP_PADDING, *self.LEFT_BOXES_SIZE
            ),
            object_id=ObjectID(object_id="#title_label", class_id="@title_label"),
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
            object_id=ObjectID(class_id="@menu_button", object_id="#new_game_btn"),
        )
        self.load_game_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="Load Game",
            anchors={"top_target": self.new_game_btn},
            object_id=ObjectID(class_id="@menu_button", object_id="#load_game_btn"),
        )
        self.delete_game_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="Delete game",
            anchors={"top_target": self.load_game_btn},
            object_id=ObjectID(class_id="@menu_button", object_id="#delete_game_btn"),
        )
        self.game_controls_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="Controls",
            anchors={"top_target": self.delete_game_btn},
            object_id=ObjectID(class_id="@menu_button", object_id="#game_controls_btn"),
        )
        self.exit_game_btn = UIButton(
            relative_rect=pygame.Rect(
                self.LEFT_PADDING, self.MENU_ITEM_SPACING, *self.LEFT_BOXES_SIZE
            ),
            manager=self.ui_manager,
            text="Exit game",
            anchors={"top_target": self.game_controls_btn},
            object_id=ObjectID(class_id="@menu_button", object_id="#exit_game_btn"),
        )

        self.games_title = UITextBox(
            relative_rect=pygame.Rect(
                self.GAMES_MARGIN_LEFT,
                self.TOP_PADDING,
                self.GAMES_WIDTH,
                self.LEFT_BOXES_SIZE[1],
            ),
            object_id=ObjectID(object_id="#games_title", class_id="@games_title"),
            html_text="Games",
            manager=self.ui_manager,
            anchors={"left_target": self.title},
        )
        self.saves_list = UISelectionList(
            relative_rect=pygame.Rect(
                self.GAMES_MARGIN_LEFT,
                self.MENU_ITEM_SPACING,
                self.GAMES_WIDTH,
                self.GAMES_HEIGHT - self.games_title.get_starting_height(),
            ),
            manager=self.ui_manager,
            item_list=[],
            object_id=ObjectID(class_id="@games_list", object_id="#games_list"),
            anchors={"top_target": self.games_title, "left_target": self.title},
        )
        self.update_saves()
        self.deletion_dialog = None

    def update_saves(self):
        self.saves = dict()
        for save in get_saves():
            save_name = save["name"]
            score = save["score"]
            list_name = f"{save_name}. Score: {score}"
            self.saves[list_name] = save_name
        self.saves_list.set_item_list([i for i in self.saves])

    DIALOG_WINDOW_SIZE = 250, 100

    def get_rect_for_dialog(self):
        MW, MH = self.DIALOG_WINDOW_SIZE
        return pygame.Rect((W - MW) // 2, (H - MH) // 2, MW, MH)

    def process_naming(self, dialog: GetSaveNameDialog):
        name = dialog.get_text()
        if name in self.saves.values():
            UIMessageWindow(
                rect=self.get_rect_for_dialog(),
                html_message="Game with such name exists",
                manager=self.ui_manager,
            )
        else:
            self.context.launch_game_scene(name)

    def render(self, screen: Surface):
        super().render(screen)

    def load_game(self):
        selected = self.get_selected()
        if selected is not None:
            self.context.launch_game_scene(self.saves[selected])

    def process_event(self, e):
        super().process_event(e)
        if e.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            self.delete_save()

    def delete_save(self):
        selected = self.get_selected()
        delete_game(self.saves[selected])
        self.update_saves()

    def get_selected(self):
        return self.saves_list.get_single_selection()

    def update(self, dt):
        super().update(dt)
        if self.new_game_btn.check_pressed():
            dialog = GetSaveNameDialog(self.ui_manager)
            dialog.accept.connect(lambda: self.process_naming(dialog))
        if self.load_game_btn.check_pressed():
            self.load_game()
        if self.exit_game_btn.check_pressed():
            self.context.exit()
        if self.delete_game_btn.check_pressed():
            selected = self.get_selected()
            if selected is not None:
                self.deletion_dialog = UIConfirmationDialog(
                    rect=self.get_rect_for_dialog(),
                    action_long_desc="Are you sure you want delete save?",
                    manager=self.ui_manager,
                    window_title="Delete operation",
                )
