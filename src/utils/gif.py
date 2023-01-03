from typing import List

import pygame
from PIL import ImageSequence, Image
from src.settings import get_path_to_image


def pil_image_to_surface(pil_image) -> pygame.Surface:
    mode, size, data = pil_image.mode, pil_image.size, pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


def load_gif(filename) -> List[pygame.Surface]:
    pil_image = Image.open(get_path_to_image(filename))
    frames = []
    if pil_image.format == "GIF" and pil_image.is_animated:
        for frame in ImageSequence.Iterator(pil_image):
            pygame_image = pil_image_to_surface(frame.convert("RGBA"))
            frames.append(pygame_image)
    else:
        frames.append(pil_image_to_surface(pil_image))
    return frames
