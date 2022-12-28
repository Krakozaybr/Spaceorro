from abc import ABC
from typing import Tuple, Sequence


class AbstractEntityConfig(ABC):
    MASS: float
    MAX_SPEED: float
    MAX_ROTATION_SPEED: float
    VERTICES: Sequence[Tuple[float, float]]
    STANDARD_START_HEALTH: float
    HEIGHT: float
    WIDTH: float
