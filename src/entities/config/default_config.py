from .abstract_config import AbstractEntityConfig
from src.settings import get_entity_config


class DefaultEntityConfig(AbstractEntityConfig):
    def __init__(self, name: str):
        data = get_entity_config(name)
        self.MASS = data["mass"]
        self.VERTICES = data["vertices"]
