from abc import ABC, abstractmethod
from typing import Type, Optional

from pygame import Surface

from src.scenes.abstract import Scene


class Context(ABC):
    @abstractmethod
    def change_scene(self, sender: Scene, target: Type[Scene], **kwargs):
        pass

    @abstractmethod
    def launch_main_menu_scene(self):
        pass

    @abstractmethod
    def launch_game_scene(self, save_name: str):
        pass

    @abstractmethod
    def launch_game_menu_scene(self, game_scene: Scene):
        pass

    @abstractmethod
    def set_scene(self, scene: Scene):
        pass

    @abstractmethod
    def screenshot(self) -> Surface:
        pass

    @abstractmethod
    def exit(self):
        pass


class ContextScene(Scene, ABC):

    context: Context

    def __init__(self, context: Context, theme_path: Optional[str] = None):
        super().__init__(theme_path)
        self.context = context
