from typing import Dict

from .basic import BasicMap


maps = {BasicMap.__name__: BasicMap}


def map_from_dict(data: Dict):
    return maps[data["class_name"]].from_dict(data)
