from abc import ABC
from typing import Tuple, Sequence


class AbstractEntityConfig(ABC):
    MASS: float
    VERTICES: Sequence[Tuple[float, float]]
