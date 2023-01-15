from abc import abstractmethod, ABC
from typing import Optional

from pygame_gui import UIManager

from src.abstract import Updateable
from src.settings import W, H
from pygame import Surface


class Scene(Updateable, ABC):

    ui_manager: UIManager

    def __init__(self, theme_path: Optional[str] = None):
        if theme_path is not None:
            self.ui_manager = UIManager((W, H), theme_path=theme_path)
        else:
            self.ui_manager = UIManager((W, H))

    @abstractmethod
    def render(self, screen: Surface):
        self.ui_manager.draw_ui(screen)

    @abstractmethod
    def update(self, dt: float):
        self.ui_manager.update(dt)

    def process_event(self, e):
        self.ui_manager.process_events(e)
