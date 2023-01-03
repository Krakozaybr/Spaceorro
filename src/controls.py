from typing import Union, List
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
        self.mouse_pos = Vec2d.zero()

    def is_key_pressed(self, key: Union[int, List[int]]):
        if isinstance(key, int):
            return self.keys.get(key, False)
        return any(self.keys.get(i, False) for i in key)

    def set_key_pressed(self, key: int, pressed: bool):
        self.keys[key] = pressed

    def set_mouse_pressed(self, button: int, state: bool):
        self.mouse_pressed[button] = state

    def is_mouse_pressed(self, button=LEFT_MOUSE_BTN):
        return self.mouse_pressed[button]

    def set_mouse_pos(self, pos: Vec2d):
        self.mouse_pos = pos

    def get_mouse_pos(self):
        return self.mouse_pos
