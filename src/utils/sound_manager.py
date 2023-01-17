import os.path

import pygame.mixer

from src.settings import SOUNDS_DIR
from src.utils.decorators import singleton


@singleton
class SoundManager:
    def __init__(self):
        self._bullet_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "bullet_sound.mp3"))
        self._death_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "death_sound.mp3"))
        self._shoot_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "shoot_sound.mp3"))
        self._cur_channel = 0

    def get_channel_index(self):
        self._cur_channel = self._cur_channel % pygame.mixer.get_num_channels()
        self._cur_channel += 1
        return self._cur_channel - 1

    def play_bullet_sound(self):
        pygame.mixer.Channel(self.get_channel_index()).play(self._bullet_sound)

    def play_death_sound(self):
        pygame.mixer.Channel(self.get_channel_index()).play(self._death_sound)

    def play_shoot_sound(self):
        pygame.mixer.Channel(self.get_channel_index()).play(self._shoot_sound)
