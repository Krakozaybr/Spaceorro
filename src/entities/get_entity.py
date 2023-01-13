from typing import Dict

from src.entities.asteroids.circle_asteroid import CircleAsteroid
from src.entities.asteroids.polygon_asteroid import PolygonAsteroid
from src.entities.gadgets.weapon.bullets.blaster_charge import BlasterCharge
from src.entities.spaceships.pallarians import PallariansCruiser

entities_classes = [PallariansCruiser, BlasterCharge, CircleAsteroid, PolygonAsteroid]
entities_dict = {i.__name__: i for i in entities_classes}


def entity_from_dict(data: Dict):
    return entities_dict[data["class_name"]].from_dict(data)
