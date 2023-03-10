from abc import ABC, abstractmethod
from typing import Dict, Optional

from src.entities.abstract.abstract import Entity
from src.entities.basic_entity.basic_spaceship import BasicSpaceship
from src.entities.pickupable.abstract import Pickupable
from src.entities.pickupable.resource import PickupableResource
from src.entities.pilots.abstract import Pilot
from src.entities.teams import Team
from src.resources import Resources
from src.utils.signal import Signal, SignalFieldMixin


class BasicPilot(Pilot, SignalFieldMixin, ABC):
    entity: BasicSpaceship
    toast = Signal()

    def __init__(
        self,
        entity: BasicSpaceship,
        team: Team,
        _obj_id: Optional[int] = None,
        resources: Optional[Resources] = None,
    ):
        super().__init__(_obj_id)
        self.entity = entity
        self.team = team
        if resources is None:
            resources = Resources()
        self.resources = resources

    def pick_up(self, item: Pickupable):
        if isinstance(item, PickupableResource):
            self.resources += item.resource

    @classmethod
    def get_default_params(cls, data: Dict) -> Dict:
        return {
            "entity": Entity.store[data["spaceship_id"]],
            "_obj_id": data["obj_id"],
            "resources": Resources.from_dict(data["resources"]),
            "team": Team(data["team"]),
        }

    def to_dict(self) -> Dict:
        return {
            **super().to_dict(),
            "spaceship_id": self.entity.obj_id,
            "obj_id": self.obj_id,
            "resources": self.resources.to_dict(),
            "team": self.team.value,
        }
