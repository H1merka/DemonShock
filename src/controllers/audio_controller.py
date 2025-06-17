# controllers/audio_controller.py

import pygame
from src.models.settings import DEFAULT_MUSIC_VOLUME, DEFAULT_SFX_VOLUME


class AudioManager:
    _music_volume = DEFAULT_MUSIC_VOLUME
    _sfx_volume = DEFAULT_SFX_VOLUME

    _current_music = None
    _sfx_cache = {}
    _weapon_sfx = {}
    _enemy_spawn_sfx = {}
    _boss_spawn_sfx = {}
    _step_sfx = None
    _step_channel = None


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
        for sfx in cls._weapon_sfx.values():
            sfx.set_volume(cls._sfx_volume)
        for sfx in cls._enemy_spawn_sfx.values():
            sfx.set_volume(cls._sfx_volume)
        for sfx in cls._boss_spawn_sfx.values():
            sfx.set_volume(cls._sfx_volume)

    @classmethod
    def get_sfx_volume(cls):
        return cls._sfx_volume

    # ===== Звуки оружия =====

    @classmethod
    def load_weapon_sfx(cls, weapon_name, filepath):
        """Загружает звук выстрела для конкретного оружия."""
        if weapon_name not in cls._weapon_sfx:
            cls._weapon_sfx[weapon_name] = pygame.mixer.Sound(filepath)
            cls._weapon_sfx[weapon_name].set_volume(cls._sfx_volume)

    @classmethod
    def play_weapon_sfx(cls, weapon_name):
        """Воспроизводит звук выстрела для оружия, если загружен."""
        if weapon_name in cls._weapon_sfx:
            cls._weapon_sfx[weapon_name].play()

    # ===== Звуки появления врагов =====

    @classmethod
    def load_enemy_spawn_sfx(cls, enemy_type, filepath):
        if enemy_type not in cls._enemy_spawn_sfx:
            cls._enemy_spawn_sfx[enemy_type] = pygame.mixer.Sound(filepath)
            cls._enemy_spawn_sfx[enemy_type].set_volume(cls._sfx_volume)

    @classmethod
    def play_enemy_spawn_sfx(cls, enemy_type):
        if enemy_type in cls._enemy_spawn_sfx:
            cls._enemy_spawn_sfx[enemy_type].play()

    @classmethod
    def load_boss_spawn_sfx(cls, boss_type, filepath):
        if boss_type not in cls._boss_spawn_sfx:
            cls._boss_spawn_sfx[boss_type] = pygame.mixer.Sound(filepath)
            cls._boss_spawn_sfx[boss_type].set_volume(cls._sfx_volume)

    @classmethod
    def play_boss_spawn_sfx(cls, boss_type):
        if boss_type in cls._boss_spawn_sfx:
            cls._boss_spawn_sfx[boss_type].play()

    @classmethod
    def load_step_sfx(cls, filepath):
        if cls._step_sfx is None:
            cls._step_sfx = pygame.mixer.Sound(filepath)
            cls._step_sfx.set_volume(cls._sfx_volume)

    @classmethod
    def play_step_sfx(cls):
        if cls._step_sfx and (cls._step_channel is None or not cls._step_channel.get_busy()):
            cls._step_channel = cls._step_sfx.play(loops=-1)

    @classmethod
    def stop_step_sfx(cls):
        if cls._step_channel:
            cls._step_channel.stop()
            cls._step_channel = None
