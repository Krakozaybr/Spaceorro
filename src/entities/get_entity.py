from typing import Dict

from src.entities.asteroids.circle_asteroid import CircleAsteroid
from src.entities.asteroids.polygon_asteroid import PolygonAsteroid
from src.entities.gadgets.weapon.bullets.blaster_charge import BlasterCharge
from src.entities.pickupable.resource import PickupableResource
from src.entities.spaceships.pallarians import *
from src.entities.spaceships.robotors import *
from src.entities.spaceships.bloodhunters import *
from src.entities.spaceships.aliens import *
from src.entities.spaceships.aquamarins import *

entities_classes = [
    BlasterCharge,
    CircleAsteroid,
    PolygonAsteroid,
    PickupableResource,
    RobotorDrone,
    RobotorBattleship,
    RobotorMiner,
    RobotorMothership,
    PallariansCruiser,
    PallariansDestroyer,
    PallariansDreadnought,
    PallariansMothership,
    AquamarinsDrone,
    AquamarinsBattleship,
    AquamarinsCruiser,
    AquamarinsDestroyer,
    AquamarinsDreadnought,
    AquamarinsMothership,
    BloodhuntersDrone,
    BloodhuntersCorvette,
    BloodhuntersCruiser,
    BloodhuntersDroneBase,
    AliensCorvette,
    AliensDrone,
    AliensMothership,
]
entities_dict = {i.__name__: i for i in entities_classes}


def entity_from_dict(data: Dict):
    return entities_dict[data["class_name"]].from_dict(data)
