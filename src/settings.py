import os
import json


SRC_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SRC_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
SAVES_DIR = os.path.join(DATA_DIR, "saves")
SOUNDS_DIR = os.path.join(DATA_DIR, "sounds")
FPS = 60
SIZE = W, H = 800, 500


def get_json(path: str):
    with open(path, encoding="utf-8") as r:
        return json.load(r)


def get_entity_config(name: str):
    entity_configs_directory = os.path.join(DATA_DIR, "configs/entities")
    config_path = os.path.join(entity_configs_directory, name)
    return get_json(config_path)


def get_entity_start_config(name: str):
    entity_start_configs_directory = os.path.join(DATA_DIR, "configs/start_entities")
    config_path = os.path.join(entity_start_configs_directory, name)
    return get_json(config_path)


def save_game(name: str, data: str) -> None:
    with open(os.path.join(SAVES_DIR, f"{name}.json"), mode="w", encoding="utf-8") as w:
        w.write(data)


def load_game(name: str) -> str:
    with open(os.path.join(SAVES_DIR, f"{name}.json"), mode="r", encoding="utf-8") as r:
        return r.read()


# DEBUG
general_config = get_json(os.path.join(DATA_DIR, "configs/general.json"))
debug_data = general_config["debug"]
DEBUG = debug_data["active"]
SHOW_VELOCITY_VECTOR = DEBUG and debug_data["show_velocity_vector"]
SHOW_CLUSTERS_BORDERS = DEBUG and debug_data["show_clusters_borders"]
SHOW_PLAYER_COLLISION_POLY = DEBUG and debug_data["show_player_collision_poly"]
