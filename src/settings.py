import os
import json
from typing import Dict, List

import pygame.image
from pygame import Surface

SRC_DIR = os.path.dirname(__file__)
CONFIGS_DIR = os.path.join(SRC_DIR, "configs")
DATA_DIR = os.path.join(SRC_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
SAVES_DIR = os.path.join(DATA_DIR, "saves")
SOUNDS_DIR = os.path.join(DATA_DIR, "sounds")
THEMES_DIR = os.path.join(CONFIGS_DIR, "themes")
GAME_SCENE_THEME_PATH = os.path.join(THEMES_DIR, "game_scene_ui_theme.json")
GAME_MENU_SCENE_THEME_PATH = os.path.join(THEMES_DIR, "game_menu_scene_ui_theme.json")
MENU_SCENE_THEME_PATH = os.path.join(THEMES_DIR, "menu_scene_ui_theme.json")
PREVIEW_SCENE_THEME_PATH = os.path.join(THEMES_DIR, "preview_scene_ui_theme.json")


def get_json(path: str):
    with open(path, encoding="utf-8") as r:
        return json.load(r)


def get_spaceship_general_config(name: str) -> Dict:
    entity_general_configs_directory = os.path.join(CONFIGS_DIR, "spaceships/general")
    config_path = os.path.join(entity_general_configs_directory, name)
    return get_json(config_path)


def get_entity_start_config(name: str) -> Dict:
    entity_start_configs_directory = os.path.join(
        CONFIGS_DIR, "spaceships/start_entities"
    )
    config_path = os.path.join(entity_start_configs_directory, name)
    return get_json(config_path)


def get_blaster_characteristics(name: str) -> Dict:
    blasters_config_dir = os.path.join(CONFIGS_DIR, "gadgets/weapon/blasters")
    config_path = os.path.join(blasters_config_dir, name)
    return get_json(config_path)


def get_bullet_configs(name: str) -> List[Dict]:
    bullet_configs_directory = os.path.join(CONFIGS_DIR, "gadgets/weapon/bullets")
    config_path = os.path.join(bullet_configs_directory, name)
    return get_json(config_path)


def get_drills_configs() -> List[Dict]:
    config_path = os.path.join(CONFIGS_DIR, "gadgets/drills.json")
    return get_json(config_path)


def get_pickupable_config(name: str) -> Dict:
    pickupable_configs_directory = os.path.join(CONFIGS_DIR, "pickupable")
    config_path = os.path.join(pickupable_configs_directory, name)
    return get_json(config_path)


def get_asteroid_config() -> Dict:
    return get_json(os.path.join(CONFIGS_DIR, "asteroids.json"))


def get_spaceship_upgrade_config(name: str) -> Dict:
    return get_json(os.path.join(CONFIGS_DIR, f"spaceships/upgrades/{name}.json"))


def save_game(name: str, data: str) -> None:
    with open(os.path.join(SAVES_DIR, f"{name}.json"), mode="w", encoding="utf-8") as w:
        w.write(data)


def game_exists(name: str) -> bool:
    return os.path.exists(os.path.join(SAVES_DIR, f"{name}.json"))


def load_game(name: str) -> Dict:
    return get_json(os.path.join(SAVES_DIR, f"{name}.json"))


def get_path_to_image(name: str) -> str:
    return os.path.join(IMAGES_DIR, name)


def load_image(name: str) -> Surface:
    return pygame.image.load(os.path.join(IMAGES_DIR, name))


general_config = get_json(os.path.join(CONFIGS_DIR, "general.json"))

# GENERAL
FPS = general_config["fps"]
SIZE = W, H = general_config["screen_width"], general_config["screen_height"]
RESOURCES_IMAGES = general_config["resources_images"]
RESOURCES_COLORS = general_config["resources_colors"]
DUST_PARTICLE_IMAGE = general_config["general_images"]["dust_particle"]
SHOW_FPS = general_config["show_fps"]
FPS_UPDATE_TIME = general_config["fps_update_time"]
HEALTH_BAR_H = general_config["health_bar_h"]
HEALTH_BAR_FONT_SIZE = general_config["health_bar_font_size"]
HEALTH_BAR_FONT_COLOR = general_config["health_bar_font_color"]

# UI
RESOURCE_LINE_HEIGHT = general_config["resource_line_height"]
UPGRADES_BTN_HEIGHT = general_config["upgrades_btn_height"]

# DEBUG
debug_data = general_config["debug"]
DEBUG = debug_data["active"]
SHOW_VELOCITY_VECTOR = DEBUG and debug_data["show_velocity_vector"]
SHOW_CLUSTERS_BORDERS = DEBUG and debug_data["show_clusters_borders"]
SHOW_PLAYER_COLLISION_POLY = DEBUG and debug_data["show_player_collision_poly"]
SAVE_GAME = False
LOG_GENERATING = False

# MAP
MAP = general_config["map"]
VISION_DISTANCE = MAP["vision_distance"]
# Map Cluster
CLUSTER = MAP["cluster"]
CLUSTER_WIDTH = CLUSTER["width"]
CLUSTER_HEIGHT = CLUSTER["height"]
CLUSTER_SIZE = CLUSTER_WIDTH, CLUSTER_HEIGHT

# BOTS
SPACESHIP_BOT_VISION_RADIUS = general_config["spaceship_bot_vision_radius"]
