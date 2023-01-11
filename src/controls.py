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
        self.key_just_changed = dict()
        self.mouse_just_pressed = dict()

    def update(self):
        self.key_just_changed.clear()
        self.mouse_just_pressed.clear()
        self.mouse_pressed[self.MIDDLE_MOUSE_BTN_UP] = False
        self.mouse_pressed[self.MIDDLE_MOUSE_BTN_DOWN] = False
        self.mouse_pressed[self.MIDDLE_MOUSE_BTN] = False

    def is_key_pressed(self, key: Union[int, List[int]]) -> bool:
        if isinstance(key, int):
            return self.keys.get(key, False)
        return any(self.keys.get(i, False) for i in key)

    def is_key_just_down(self, key: int) -> bool:
        return self.key_just_changed.get(key, False)

    def is_mouse_just_up(self, button=LEFT_MOUSE_BTN) -> bool:
        return not self.mouse_just_pressed.get(button, True)

    def is_mouse_just_down(self, button=LEFT_MOUSE_BTN) -> bool:
        return self.mouse_just_pressed.get(button, False)

    def is_key_just_up(self, key: int) -> bool:
        return not self.key_just_changed.get(key, True)

    def set_key_pressed(self, key: int, pressed: bool):
        self.keys[key] = pressed
        self.key_just_changed[key] = pressed

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

    def is_mouse_pressed(self, button=LEFT_MOUSE_BTN):
        return self.mouse_pressed[button]

    def set_mouse_pos(self, pos: Vec2d):
        self.mouse_pos = pos

    def get_mouse_pos(self) -> Vec2d:
        return self.mouse_pos
