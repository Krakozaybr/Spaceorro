from abc import abstractmethod, ABC
from typing import Dict, Optional

from src.abstract import RenderUpdateObject
from src.entities.asteroids.abstract import AbstractAsteroid
from src.entities.gadgets.drills.config import DrillConfig
from src.settings import get_drills_configs


class AbstractDrill(RenderUpdateObject, ABC):
    configs: Dict[int, DrillConfig]
    asteroid: Optional[AbstractAsteroid]
    is_mining: bool

    @abstractmethod
    def can_mine(self, asteroid: AbstractAsteroid) -> bool:
        pass

    @abstractmethod
    def set_target(self, asteroid: AbstractAsteroid):
        pass

    @property
    def damage(self) -> float:
        return self.config.damage

    @property
    @abstractmethod
    def config(self) -> DrillConfig:
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        cls.configs = {
            data["level"]: DrillConfig.from_dict(data) for data in get_drills_configs()
        }
