from abc import ABC, abstractmethod

from src.abstract import Updateable, Serializable
from src.entities.abstract.abstract import StoreMixin, Entity
from src.entities.pickupable.abstract import Pickupable
from src.entities.teams import Team
from src.resources import Resources
from src.utils.decorators import storable


@storable
class Pilot(Updateable, StoreMixin, Serializable, ABC):
    entity: Entity
    team: Team
    resources: Resources

    @abstractmethod
    def pick_up(self, item: Pickupable):
        pass

    @property
    def is_active(self) -> bool:
        res = self.entity.is_active
        if not res:
            del self.store[self.obj_id]
        else:
            self.store[self.obj_id] = self
        return res
