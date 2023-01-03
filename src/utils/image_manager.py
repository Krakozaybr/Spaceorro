from typing import List

from pygame import Surface

from src.utils.decorators import singleton
from src.utils.gif import load_gif


@singleton
class ImageManager:

    EXPLOSION_FRAMES_FILE = "explosion.gif"
    _explosion_frames: List[Surface]

    @property
    def explosion_frames(self) -> List[Surface]:
        if not hasattr(self, "_explosion_frames"):
            self._explosion_frames = load_gif(self.EXPLOSION_FRAMES_FILE)
        return self._explosion_frames.copy()
