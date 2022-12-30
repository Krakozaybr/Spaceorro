from typing import Dict

from src.entities.abstract import Pilot, EntityView
from src.entities.config.default_config import DefaultEntityConfig
from src.entities.gadgets.engines.default_engine import DefaultEngine
from src.utils.body_serialization import apply_params_to_kinematic_body_from_dict, \
    apply_params_to_dynamic_body_from_dict
from .pilot import PlayerPilot
from .view import PlayerView
from ..basic_entity.entity import BasicEntity
from ...gadgets.engines.abstract import Engine


class PlayerEntity(BasicEntity):

    CONFIG_NAME = "player.json"
    START_CONFIG_NAME = "player.json"
    config = DefaultEntityConfig(CONFIG_NAME)

    def create_engine(self) -> Engine:
        return DefaultEngine(self, self.control_body, self.velocity_characteristics)

    def create_pilot(self) -> Pilot:
        return PlayerPilot(self)

    def create_view(self) -> EntityView:
        return PlayerView(self)

    def to_dict(self) -> Dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: Dict):
        body = data['body']
        control_body = data['control_body']
        res = PlayerEntity(
            pos=body['position'],
            mass=body['mass'],
            moment=body['moment'],
            **cls.get_characteristics(data)
        )
        apply_params_to_dynamic_body_from_dict(res, body)
        apply_params_to_kinematic_body_from_dict(res.control_body, control_body)
        return res
