from typing import Dict

from src.entities.pilots.abstract import Pilot
from src.entities.pilots.player.player import PlayerPilot

pilots = {PlayerPilot}
class_names = {i.__name__: i for i in pilots}


def get_pilot(data: Dict) -> Pilot:
    return class_names[data["class_name"]].from_dict(data)
