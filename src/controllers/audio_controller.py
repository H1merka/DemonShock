# controllers/audio_controller.py

import pygame
from src.models.settings import DEFAULT_MUSIC_VOLUME, DEFAULT_SFX_VOLUME


class AudioManager:
    _music_volume = DEFAULT_MUSIC_VOLUME
    _sfx_volume = DEFAULT_SFX_VOLUME

    _current_music = None
    _sfx_cache = {}

    @classmethod
    def init(cls):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(cls._music_volume)

    @classmethod
    def play_music(cls, music_path, loops=-1):
        if cls._current_music != music_path:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops=loops)
            cls._current_music = music_path

    @classmethod
    def stop_music(cls):
        pygame.mixer.music.stop()
        cls._current_music = None

    @classmethod
    def set_music_volume(cls, volume):
        cls._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(cls._music_volume)

    @classmethod
    def get_music_volume(cls):
        return cls._music_volume

    @classmethod
    def load_sfx(cls, name, filepath):
        """Загрузка звукового эффекта с кешированием."""
        if name not in cls._sfx_cache:
            cls._sfx_cache[name] = pygame.mixer.Sound(filepath)
            cls._sfx_cache[name].set_volume(cls._sfx_volume)

    @classmethod
    def play_sfx(cls, name):
        if name in cls._sfx_cache:
            cls._sfx_cache[name].play()

    @classmethod
    def set_sfx_volume(cls, volume):
        cls._sfx_volume = max(0.0, min(1.0, volume))
        for sfx in cls._sfx_cache.values():
            sfx.set_volume(cls._sfx_volume)

    @classmethod
    def get_sfx_volume(cls):
        return cls._sfx_volume
