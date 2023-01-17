from typing import List, Tuple, Dict, Optional, Union

import pygame.transform
from pygame import Surface

from src.settings import load_image
from src.utils.decorators import singleton
from src.utils.gif import load_gif


@singleton
class ImageManager:

    pics: Dict[str, Dict[Union[str, Tuple[int, int]], Surface]]
    gifs: Dict[str, Dict[Union[str, Tuple[int, int]], List[Surface]]]
    cropped_gifs: Dict[str, Dict[Tuple[int, int, int, int], List[Surface]]]
    default = "default"

    EXPLOSION_FRAMES_FILE = "explosion.gif"
    ALIENS_CORVETTE = "aliens corvette.png"
    ALIENS_DRONE = "aliens drone.png"
    ALIENS_MOTHERSHIP = "aliens mothership.png"
    AQUAMARINS_BATTLESHIP = "aquamarins battleship.png"
    AQUAMARINS_CRUISER = "aquamarins cruiser.png"
    AQUAMARINS_DESTROYER = "aquamarins destroyer.png"
    AQUAMARINS_DREADNOUGHT = "aquamarins dreadnought.png"
    AQUAMARINS_DRONE = "aquamarins drone.png"
    AQUAMARINS_MOTHERSHIP = "aquamarins mothership.png"
    BLOODHUNTERS_CORVETTE = "bloodhunters corvette.png"
    BLOODHUNTERS_CRUISER = "bloodhunters cruiser.png"
    BLOODHUNTERS_DRONE = "bloodhunters drone.png"
    BLOODHUNTERS_DRONE_BASE = "bloodhunters drone base.png"
    PALLARIANS_CRUISER = "pallarians cruiser.png"
    PALLARIANS_DESTROYER = "pallarians destroyer.png"
    PALLARIANS_DREADNOUGHT = "pallarians dreadnought.png"
    PALLARIANS_MOTHERSHIP = "pallarians mothership.png"
    ROBOTOR_BATTLESHIP = "robotor battleship.png"
    ROBOTOR_DRONE = "robotor drone.png"
    ROBOTOR_MINER = "robotor miner.png"
    ROBOTOR_MOTHERSHIP = "robotor mothership.png"
    TRADERS_DRONE = "traders drone.png"
    TRADERS_MOTHERSHIP = "traders mothership.png"
    TRADERS_TRADER = "traders trader.png"

    CONTROLS = 'controls.png'

    def __init__(self):
        self.pics = dict()
        self.gifs = dict()
        self.cropped_gifs = dict()

    def get_pic(
        self, name, w: Optional[int] = None, h: Optional[int] = None
    ) -> Surface:
        if w is None or h is None:
            key = self.default
        else:
            key = (w, h)
        if name not in self.pics:
            img = load_image(name)
            width, height = img.get_size()
            self.pics[name] = dict()
            self.pics[name][self.default] = img
            self.pics[name][(width, height)] = img
        if key not in self.pics[name]:
            self.pics[name][key] = pygame.transform.scale(
                self.pics[name][self.default], (w, h)
            )
        return self.pics[name][key]

    def get_gif(
        self, name: str, w: Optional[int] = None, h: Optional[int] = None
    ) -> List[Surface]:
        if w is None or h is None:
            key = self.default
        else:
            key = (w, h)
        if name not in self.gifs:
            gif = load_gif(name)
            width, height = gif[0].get_size()
            self.gifs[name] = dict()
            self.gifs[name][self.default] = gif
            self.gifs[name][(width, height)] = gif
        if key not in self.gifs[name]:
            self.gifs[name][key] = [
                pygame.transform.scale(img, (w, h))
                for img in self.gifs[name][self.default]
            ]
        return self.gifs[name][key].copy()

    def get_crop_gif(self, name: str, x: int, y: int, w: int, h: int) -> List[Surface]:
        key = (x, y, w, h)
        if name not in self.cropped_gifs:
            self.cropped_gifs[name] = dict()
        if key not in self.cropped_gifs[name]:
            gif = self.get_gif(name)
            gif_w, gif_h = gif[0].get_size()
            x = (x + gif_w) % gif_w
            y = (y + gif_h) % gif_h
            if not w:
                w = gif_w - x
            if not h:
                h = gif_h - y
            self.cropped_gifs[name][key] = [
                frame.subsurface((x, y, w, h)) for frame in gif
            ]
        return self.cropped_gifs[name][key]

    def explosion_frames(
        self, w: Optional[int] = None, h: Optional[int] = None
    ) -> List[Surface]:
        return self.get_gif(self.EXPLOSION_FRAMES_FILE, w, h)
