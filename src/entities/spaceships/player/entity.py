from typing import Dict

from src.entities.abstract.abstract import EntityView
from src.entities.gadgets.engines.default_engine import DefaultEngine
from src.entities.pilots.abstract import Pilot
from .view import PlayerView
from ...basic_entity.basic_entity import PolyBasicEntity
from ...basic_entity.basic_spaceship import BasicSpaceship
from ...gadgets.engines.abstract import Engine
from ...gadgets.weapon.blasters.blaster import Blaster
from ...pilots.get_pilot import get_pilot
from ...pilots.simple_bot import SimpleBot
from ...teams import Team


class PallariansCruiser(BasicSpaceship, PolyBasicEntity):

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
        return SimpleBot(self, Team.neutral)

    def on_explode(self):
        pass

    def to_dict(self) -> Dict:
        return super().to_dict()

    @classmethod
    def from_dict(cls, data: Dict):
        res = PallariansCruiser(
            weapon=Blaster.from_dict(data["weapon"]), **cls.get_default_params(data)
        )
        res.pilot = get_pilot(data["pilot"])
        res.apply_params_to_bodies(data)
        return res
