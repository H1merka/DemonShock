import pygame
from typing import Optional
from src.models.settings import DEFAULT_MUSIC_VOLUME, DEFAULT_SFX_VOLUME


class AudioManager:
    """
    Manages music and sound effects playback, volume control,
    and caching of loaded sounds.
    """

    _music_volume: float = DEFAULT_MUSIC_VOLUME
    _sfx_volume: float = DEFAULT_SFX_VOLUME

    _current_music: Optional[str] = None
    _sfx_cache: dict[str, pygame.mixer.Sound] = {}
    _weapon_sfx: dict[str, pygame.mixer.Sound] = {}
    _enemy_spawn_sfx: dict[str, pygame.mixer.Sound] = {}
    _boss_spawn_sfx: dict[str, pygame.mixer.Sound] = {}
    _step_sfx: Optional[pygame.mixer.Sound] = None
    _step_channel: Optional[pygame.mixer.Channel] = None

    @classmethod
    def init(cls) -> None:
        """Initialize the pygame mixer and set initial music volume."""
        pygame.mixer.init()
        pygame.mixer.music.set_volume(cls._music_volume)

    @classmethod
    def play_music(cls, music_path: str, loops: int = -1) -> None:
        """
        Load and play background music if not already playing the same track.

        Args:
            music_path (str): Path to music file.
            loops (int): Number of loops (-1 for infinite).
        """
        if cls._current_music != music_path:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops=loops)
            cls._current_music = music_path

    @classmethod
    def stop_music(cls) -> None:
        """Stop the background music playback."""
        pygame.mixer.music.stop()
        cls._current_music = None

    @classmethod
    def set_music_volume(cls, volume: float) -> None:
        """
        Set the volume for background music, clamped between 0.0 and 1.0.

        Args:
            volume (float): Volume level.
        """
        cls._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(cls._music_volume)

    @classmethod
    def get_music_volume(cls) -> float:
        """Return the current music volume."""
        return cls._music_volume

    @classmethod
    def load_sfx(cls, name: str, filepath: str) -> None:
        """
        Load a sound effect with caching.

        Args:
            name (str): Identifier for the sound effect.
            filepath (str): Path to the sound file.
        """
        if name not in cls._sfx_cache:
            cls._sfx_cache[name] = pygame.mixer.Sound(filepath)
            cls._sfx_cache[name].set_volume(cls._sfx_volume)

    @classmethod
    def play_sfx(cls, name: str) -> None:
        """
        Play a cached sound effect by name.

        Args:
            name (str): Identifier of the sound effect.
        """
        if name in cls._sfx_cache:
            cls._sfx_cache[name].play()

    @classmethod
    def set_sfx_volume(cls, volume: float) -> None:
        """
        Set volume for all loaded sound effects.

        Args:
            volume (float): Volume level.
        """
        cls._sfx_volume = max(0.0, min(1.0, volume))
        for sfx_dict in (
            cls._sfx_cache,
            cls._weapon_sfx,
            cls._enemy_spawn_sfx,
            cls._boss_spawn_sfx,
        ):
            for sfx in sfx_dict.values():
                sfx.set_volume(cls._sfx_volume)

    @classmethod
    def get_sfx_volume(cls) -> float:
        """Return the current sound effects volume."""
        return cls._sfx_volume

    # ===== Weapon sound effects =====

    @classmethod
    def load_weapon_sfx(cls, weapon_name: str, filepath: str) -> None:
        """
        Load weapon firing sound effect.

        Args:
            weapon_name (str): Name of the weapon.
            filepath (str): Path to sound file.
        """
        if weapon_name not in cls._weapon_sfx:
            cls._weapon_sfx[weapon_name] = pygame.mixer.Sound(filepath)
            cls._weapon_sfx[weapon_name].set_volume(cls._sfx_volume)

    @classmethod
    def play_weapon_sfx(cls, weapon_name: str) -> None:
        """
        Play weapon firing sound effect if loaded.

        Args:
            weapon_name (str): Name of the weapon.
        """
        if weapon_name in cls._weapon_sfx:
            cls._weapon_sfx[weapon_name].play()

    # ===== Enemy spawn sound effects =====

    @classmethod
    def load_enemy_spawn_sfx(cls, enemy_type: str, filepath: str) -> None:
        """
        Load enemy spawn sound effect.

        Args:
            enemy_type (str): Type of enemy.
            filepath (str): Path to sound file.
        """
        if enemy_type not in cls._enemy_spawn_sfx:
            cls._enemy_spawn_sfx[enemy_type] = pygame.mixer.Sound(filepath)
            cls._enemy_spawn_sfx[enemy_type].set_volume(cls._sfx_volume)

    @classmethod
    def play_enemy_spawn_sfx(cls, enemy_type: str) -> None:
        """
        Play enemy spawn sound effect if loaded.

        Args:
            enemy_type (str): Type of enemy.
        """
        if enemy_type in cls._enemy_spawn_sfx:
            cls._enemy_spawn_sfx[enemy_type].play()

    # ===== Boss spawn sound effects =====

    @classmethod
    def load_boss_spawn_sfx(cls, boss_type: str, filepath: str) -> None:
        """
        Load boss spawn sound effect.

        Args:
            boss_type (str): Type of boss.
            filepath (str): Path to sound file.
        """
        if boss_type not in cls._boss_spawn_sfx:
            cls._boss_spawn_sfx[boss_type] = pygame.mixer.Sound(filepath)
            cls._boss_spawn_sfx[boss_type].set_volume(cls._sfx_volume)

    @classmethod
    def play_boss_spawn_sfx(cls, boss_type: str) -> None:
        """
        Play boss spawn sound effect if loaded.

        Args:
            boss_type (str): Type of boss.
        """
        if boss_type in cls._boss_spawn_sfx:
            cls._boss_spawn_sfx[boss_type].play()

    # ===== Step sound effect =====

    @classmethod
    def load_step_sfx(cls, filepath: str) -> None:
        """
        Load looping step sound effect.

        Args:
            filepath (str): Path to sound file.
        """
        if cls._step_sfx is None:
            cls._step_sfx = pygame.mixer.Sound(filepath)
            cls._step_sfx.set_volume(cls._sfx_volume)

    @classmethod
    def play_step_sfx(cls) -> None:
        """
        Play looping step sound effect if not already playing.
        """
        if cls._step_sfx and (cls._step_channel is None or not cls._step_channel.get_busy()):
            cls._step_channel = cls._step_sfx.play(loops=-1)

    @classmethod
    def stop_step_sfx(cls) -> None:
        """
        Stop the looping step sound effect if playing.
        """
        if cls._step_channel:
            cls._step_channel.stop()
            cls._step_channel = None
