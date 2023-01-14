from typing import Dict, Optional

from pygame.sprite import AbstractGroup
from pymunk import Vec2d

from src.entities.abstract.abstract import EntityView, Entity, SaveStrategy
from src.entities.basic_entity.view import BasicView
from src.entities.entity_configs import PickupableEntityConfig
from src.entities.modifiers_and_characteristics import (
    TemporaryObjectLifeCharacteristics,
)
from src.entities.pickupable.abstract import Pickupable
from src.resources import ResourceType, Resource
from src.settings import get_pickupable_config


class PickupableResourceView(BasicView):

    entity: Pickupable

    def __init__(
        self, entity: Entity, resource_type: ResourceType, *groups: AbstractGroup
    ):
        super().__init__(entity, *groups)
        self.image = resource_type.get_image(int(self.w), int(self.h))

    def init_sizes(self):
        self.w = self.entity.config.radius
        self.h = self.entity.config.radius
        self.right_top_corner_delta = Vec2d(-self.w / 2, -self.h / 2)


class PickupableResource(Pickupable):

    view: PickupableResourceView
    resource: Resource
    config_name = "resource.json"
    config = PickupableEntityConfig.from_dict(get_pickupable_config(config_name))
    save_strategy = SaveStrategy.ENTITY

    def __init__(
        self,
        pos: Vec2d,
        resource: Resource,
        life_characteristics: Optional[TemporaryObjectLifeCharacteristics] = None,
        moment: Optional[float] = None,
        entity_id: Optional[int] = None,
    ):
        self.resource = resource
        super().__init__(
            pos=pos,
            life_characteristics=life_characteristics,
            mass=self.create_mass(),
            moment=moment,
            entity_id=entity_id,
        )

    def create_view(self) -> EntityView:
        return PickupableResourceView(self, self.resource.resource_type)

    def create_mass(self) -> float:
        return 1

    def take_damage(self, damage: float) -> None:
        pass

    @classmethod
    def from_dict(cls, data: Dict):
        res = PickupableResource(
            pos=data["body"]["position"],
            entity_id=data["id"],
            resource=Resource.from_dict(data["resource"]),
            **cls.get_characteristics(data)
        )
        res.apply_params_to_bodies(data)
        return res

    def to_dict(self) -> Dict:
        return {**super().to_dict(), "resource": self.resource.to_dict()}

    @staticmethod
    def get_characteristics(data: Dict) -> Dict:
        return {
            "life_characteristics": TemporaryObjectLifeCharacteristics.from_dict(
                data["life_characteristics"]
            ),
        }
