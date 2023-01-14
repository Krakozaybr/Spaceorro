from abc import ABC, abstractmethod
from typing import Type

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
    def screenshot(self) -> Surface:
        pass


class ContextScene(Scene, ABC):

    context: Context

    def __init__(self, context: Context):
        super().__init__()
        self.context = context
