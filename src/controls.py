from typing import Union, List


class Controls:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__init__()
        return cls.__instance

    @classmethod
    def get_instance(cls):
        return cls.__new__(cls)

    def __init__(self):
        self.keys = dict()

    def is_key_pressed(self, key: Union[int, List[int]]):
        if isinstance(key, int):
            return self.keys.get(key, False)
        return any(self.keys.get(i, False) for i in key)

    def set_key_pressed(self, key: int, pressed: bool):
        self.keys[key] = pressed
