from typing import Union, List

import pygame_gui.elements
from pymunk import Vec2d

from src.utils.decorators import singleton


@singleton
class Controls:

    LEFT_MOUSE_BTN = 1
    MIDDLE_MOUSE_BTN = 2
    RIGHT_MOUSE_BTN = 3
    MIDDLE_MOUSE_BTN_UP = 4
    MIDDLE_MOUSE_BTN_DOWN = 5
    EXTRA_MOUSE_BTN_1 = 6
    EXTRA_MOUSE_BTN_2 = 7

    def __init__(self):
        self.keys = dict()
        self.mouse_pressed = {
            self.LEFT_MOUSE_BTN: False,
            self.MIDDLE_MOUSE_BTN: False,
            self.RIGHT_MOUSE_BTN: False,
            self.MIDDLE_MOUSE_BTN_UP: False,
            self.MIDDLE_MOUSE_BTN_DOWN: False,
            self.EXTRA_MOUSE_BTN_1: False,
            self.EXTRA_MOUSE_BTN_2: False,
        }
        self.buttons = dict()

        self.key_just_changed = dict()
        self.mouse_just_pressed = dict()

        self.mouse_pos = Vec2d.zero()

    def update(self):
        self.key_just_changed.clear()
        self.mouse_just_pressed.clear()
        self.buttons.clear()
        self.mouse_pressed[self.MIDDLE_MOUSE_BTN_UP] = False
        self.mouse_pressed[self.MIDDLE_MOUSE_BTN_DOWN] = False
        self.mouse_pressed[self.MIDDLE_MOUSE_BTN] = False

    # Keys
    def is_key_pressed(self, key: Union[int, List[int]]) -> bool:
        if isinstance(key, int):
            return self.keys.get(key, False)
        return any(self.keys.get(i, False) for i in key)

    def is_key_just_down(self, key: int) -> bool:
        return self.key_just_changed.get(key, False)

    def is_key_just_up(self, key: int) -> bool:
        return not self.key_just_changed.get(key, True)

    def set_key_pressed(self, key: int, pressed: bool):
        self.keys[key] = pressed
        self.key_just_changed[key] = pressed

    # Mouse
    def is_mouse_just_up(self, button=LEFT_MOUSE_BTN) -> bool:
        return not self.mouse_just_pressed.get(button, True)

    def is_mouse_just_down(self, button=LEFT_MOUSE_BTN) -> bool:
        return self.mouse_just_pressed.get(button, False)

    def set_mouse_pressed(self, button: int, state: bool):
        self.mouse_pressed[button] = state
        if button in [
            self.MIDDLE_MOUSE_BTN_UP,
            self.MIDDLE_MOUSE_BTN_DOWN,
            self.MIDDLE_MOUSE_BTN,
        ]:
            self.mouse_just_pressed[button] = True
        else:
            self.mouse_just_pressed[button] = state

    def is_mouse_pressed(self, button: Union[List[int], int] = LEFT_MOUSE_BTN):
        if isinstance(button, int):
            return self.mouse_pressed.get(button, False)
        return any(self.mouse_pressed.get(i, False) for i in button)

    def set_mouse_pos(self, pos: Vec2d):
        self.mouse_pos = pos

    def get_mouse_pos(self) -> Vec2d:
        return self.mouse_pos

    # GUI
    def set_button_pressed(self, button: pygame_gui.elements.UIButton):
        self.buttons[button] = True

    def is_button_pressed(self, button: pygame_gui.elements.UIButton) -> bool:
        return self.buttons.get(button, False)
