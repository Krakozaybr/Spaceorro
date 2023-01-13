from dataclasses import dataclass

from src.utils.serializable_dataclass import SerializableDataclass


@dataclass
class DrillConfig(SerializableDataclass):
    level: int
    gif: str
    damage: float
    mining_distance: float
    animation_height: float
