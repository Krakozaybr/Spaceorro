import os
import json

SRC_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SRC_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
SAVES_DIR = os.path.join(DATA_DIR, "saves")
SOUNDS_DIR = os.path.join(DATA_DIR, "sounds")
FPS = 60
SIZE = W, H = 800, 500


def get_entity_config(name: str):
    entity_configs_directory = os.path.join(DATA_DIR, "configs/entities")
    config_path = os.path.join(entity_configs_directory, name)
    with open(config_path, encoding="utf-8") as r:
        return json.load(r)
