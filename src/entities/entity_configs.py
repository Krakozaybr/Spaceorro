from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Sequence

from src.settings import get_spaceship_general_config
from src.utils.serializable_dataclass import SerializableDataclass


@dataclass
class AbstractEntityConfig(SerializableDataclass, ABC):
    pass


@dataclass
class EntityWithFixedMassConfig(AbstractEntityConfig):
    mass: float


@dataclass
class PolyEntityConfig(EntityWithFixedMassConfig, ABC):
    vertices: Sequence[Tuple[float, float]]


@dataclass
class SpaceshipEntityConfig(PolyEntityConfig):
    blaster_relative_position: Tuple[float, float]

    @classmethod
    def load(cls, name: str):
        return cls.from_dict(get_spaceship_general_config(name))


@dataclass
class BulletEntityConfig(EntityWithFixedMassConfig):
    radius: float
    level: int
    damage: float
    speed: float
    life_time: float
    explosion_radius: float
    image: str


@dataclass
class PickupableEntityConfig(AbstractEntityConfig):
    radius: float
    life_time: float


@dataclass
class AsteroidEntityConfig(AbstractEntityConfig):
    mining_health_area_coef: float
    mass_coef: float
    health_area_coef: float
    radius_interval: Tuple[int, int]
    vertices_count: Tuple[int, int]
    polygons_count: Tuple[int, int]
    frequency: float
    losses_coef: float
