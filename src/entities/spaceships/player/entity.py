from typing import Dict

from src.entities.abstract.abstract import Pilot, EntityView
from src.entities.gadgets.engines.default_engine import DefaultEngine
from src.utils.body_serialization import (
    apply_params_to_kinematic_body_from_dict,
    apply_params_to_dynamic_body_from_dict,
)
from src.entities.pilots.player import PlayerPilot
from .view import PlayerView
from ...basic_entity.basic_entity import PolyBasicEntity
from ...basic_entity.basic_spaceship import BasicSpaceship
from ...gadgets.engines.abstract import Engine
from ...gadgets.weapon.blasters.blaster import Blaster
from ...pilots import get_pilot


class PlayerEntity(BasicSpaceship, PolyBasicEntity):

    # static fields
    config_name = "player.json"
    start_config_name = "player.json"

    def create_engine(self) -> Engine:
        return DefaultEngine(self, self.control_body, self.velocity_characteristics)

    def create_view(self) -> EntityView:
        return PlayerView(self)

    def create_weapon(self) -> Blaster:
        return Blaster.create_simple_blaster(self)

    def create_pilot(self) -> Pilot:
        return PlayerPilot(self)

    def to_dict(self) -> Dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: Dict):
        body = data["body"]
        control_body = data["control_body"]
        res = PlayerEntity(
            pos=body["position"],
            mass=body["mass"],
            moment=body["moment"],
            weapon=Blaster.from_dict(data["weapon"]),
            entity_id=int(data["id"]),
            **cls.get_characteristics(data),
        )
        res.pilot = get_pilot(data["pilot"])
        apply_params_to_dynamic_body_from_dict(res, body)
        apply_params_to_kinematic_body_from_dict(res.control_body, control_body)
        return res
