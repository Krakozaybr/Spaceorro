from typing import Dict

from src.entities.gadgets.weapon.bullets.blaster_charge import BlasterCharge
from src.entities.spaceships.player.entity import PlayerEntity

entities_classes = [PlayerEntity, BlasterCharge]
entities_dict = {i.__name__: i for i in entities_classes}


def entity_from_dict(data: Dict):
    return entities_dict[data["class_name"]].from_dict(data)
