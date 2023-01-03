from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Sequence

from src.settings import get_spaceship_general_config
from src.utils.serializable_dataclass import SerializableDataclass


@dataclass
class AbstractEntityConfig(SerializableDataclass, ABC):
    mass: float


@dataclass
class PolyEntityConfig(AbstractEntityConfig, ABC):
    vertices: Sequence[Tuple[float, float]]


@dataclass
class SpaceshipEntityConfig(PolyEntityConfig):
    blaster_relative_position: Tuple[float, float]

    @classmethod
    def load(cls, name: str):
        return cls.from_dict(get_spaceship_general_config(name))


@dataclass
class BulletEntityConfig(AbstractEntityConfig):
    radius: float
    level: int
    damage: float
    speed: float
    life_time: float
    explosion_radius: float
    image: str
