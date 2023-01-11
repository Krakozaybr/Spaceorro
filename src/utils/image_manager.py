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
    default = "default"

    EXPLOSION_FRAMES_FILE = "explosion.gif"

    def __init__(self):
        self.pics = dict()
        self.gifs = dict()

    def get_pic(self, name, w: Optional[int] = None, h: Optional[int] = None):
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

    def get_gif(self, name: str, w: Optional[int] = None, h: Optional[int] = None):
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

    def explosion_frames(
        self, w: Optional[int] = None, h: Optional[int] = None
    ) -> List[Surface]:
        return self.get_gif(self.EXPLOSION_FRAMES_FILE, w, h)
