from src.entities.abstract import Pilot, EntityView
from src.entities.config.default_config import DefaultEntityConfig
from src.entities.gadgets.engines.default_engine import DefaultEngine
from .pilot import PlayerPilot
from .view import PlayerView
from ..basic_entity.entity import BasicEntity
from ...gadgets.engines.abstract import Engine


class PlayerEntity(BasicEntity):

    CONFIG_NAME = "player.json"
    START_CONFIG_NAME = "player.json"
    config = DefaultEntityConfig(CONFIG_NAME)

    def create_engine(self) -> Engine:
        return DefaultEngine(
            self, self.control_body, self.velocity_characteristics
        )

    def create_pilot(self) -> Pilot:
        return PlayerPilot(self)

    def create_view(self) -> EntityView:
        return PlayerView(self)

    def serialize(self) -> str:
        ...

    @staticmethod
    def deserialize(data: str):
        ...
