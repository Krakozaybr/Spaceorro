from typing import Dict

from .player import PlayerPilot
from ..abstract.abstract import Pilot

pilots = {PlayerPilot}
class_names = {i.__name__: i for i in pilots}


def get_pilot(data: Dict) -> Pilot:
    return class_names[data["class_name"]].from_dict(data)
