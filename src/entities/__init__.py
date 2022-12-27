from .player.entity import PlayerEntity
import json


entities_classes = [PlayerEntity]
entities_dict = {i.__name__: i for i in entities_classes}


def deserialize(data: str):
    data = json.loads(data)
    return entities_dict[data["class_name"]].deserialize(data)
