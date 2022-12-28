from .abstract_config import AbstractEntityConfig
from src.settings import get_entity_config


class DefaultEntityConfig(AbstractEntityConfig):
    def __init__(self, name: str):
        data = get_entity_config(name)
        self.MASS = data["mass"]
        self.MAX_SPEED = data["max_speed"]
        self.MAX_ROTATION_SPEED = data["max_rotation_speed"]
        self.VERTICES = data["vertices"]
        self.HEIGHT = data["height"]
        self.WIDTH = data["width"]
        self.STANDARD_START_HEALTH = data["standard_start_health"]
