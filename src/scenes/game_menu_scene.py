import pygame.draw
from pygame import Surface
from pygame_gui.elements import UIPanel, UIButton, UILabel

from .context import ContextScene, Context
from .game.game_scene import GameScene
from ..controls import Controls
from ..settings import GAME_MENU_SCENE_THEME_PATH, save_game


class GameMenuScene(ContextScene):
    def __init__(self, context: Context, game_scene: GameScene):
        super().__init__(context, theme_path=GAME_MENU_SCENE_THEME_PATH)
        self.game_scene = game_scene

        # Background
        self.background = context.screenshot()
        self.blackout = Surface(self.background.get_size(), pygame.SRCALPHA)
        self.blackout.fill((0, 0, 0, 255 // 2))

        # GUI
        btn_rect = pygame.Rect(-3, 0, 180, 50)

        self.panel = UIPanel(
            relative_rect=pygame.Rect(0, 0, 200, 200),
            manager=self.ui_manager,
            anchors={"center": "center"},
        )

        self.menu_text = UILabel(
            text="Menu",
            relative_rect=pygame.Rect(0, 0, 100, 100),
            anchors={"centerx": "centerx", "target_bottom": self.panel},
            manager=self.ui_manager,
        )
        self.continue_btn = UIButton(
            text="Continue",
            relative_rect=btn_rect.copy(),
            manager=self.ui_manager,
            container=self.panel,
            anchors={"top": "top", "centerx": "centerx"},
        )
        self.save_btn = UIButton(
            text="Save",
            relative_rect=btn_rect.copy(),
            manager=self.ui_manager,
            container=self.panel,
            anchors={"top_target": self.continue_btn, "centerx": "centerx"},
        )
        self.exit_btn = UIButton(
            text="Exit",
            relative_rect=btn_rect.copy(),
            manager=self.ui_manager,
            container=self.panel,
            anchors={"top_target": self.save_btn, "centerx": "centerx"},
        )

    def render(self, screen: Surface):
        # Background
        screen.blit(self.background, (0, 0))
        screen.blit(self.blackout, (0, 0))

        # GUI
        super().render(screen)

    def update(self, dt):
        super().update(dt)
        if (
            Controls().is_key_just_down(pygame.K_ESCAPE)
            or self.continue_btn.check_pressed()
        ):
            self.context.set_scene(self.game_scene)
        if self.save_btn.check_pressed():
            save_game(
                self.game_scene.name,
                self.game_scene.serialize(),
                self.game_scene.player.score,
            )
        if self.exit_btn.check_pressed():
            self.context.launch_main_menu_scene()
