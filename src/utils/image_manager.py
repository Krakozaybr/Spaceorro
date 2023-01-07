from typing import List, Tuple, Dict, Optional

import pygame.transform
from pygame import Surface

from src.utils.decorators import singleton
from src.utils.gif import load_gif


@singleton
class ImageManager:

    EXPLOSION_FRAMES_FILE = "explosion.gif"
    _explosion_frames: Dict[Tuple[int, int], List[Surface]]
    _explosion_frames_default: List[Surface]

    def explosion_frames(
        self, w: Optional[int] = None, h: Optional[int] = None
    ) -> List[Surface]:
        if not hasattr(self, "_explosion_frames"):
            self._explosion_frames_default = gif = load_gif(self.EXPLOSION_FRAMES_FILE)
            width, height = gif[0].get_width(), gif[0].get_height()
            self._explosion_frames = {(width, height): gif}
        if w is None or h is None:
            return self._explosion_frames_default.copy()
        if (w, h) not in self._explosion_frames:
            self._explosion_frames[w, h] = [
                pygame.transform.scale(frame, (w, h))
                for frame in self._explosion_frames_default
            ]
        return self._explosion_frames[w, h].copy()
