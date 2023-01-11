from typing import Dict

from src.entities.pilots.basic_pilot import BasicPilot


class SimpleBot(BasicPilot):
    def update(self, dt: float):
        pass

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**super().get_default_params(data))
