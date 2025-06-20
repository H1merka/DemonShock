import pygame
from typing import Optional, Dict, Any
from src.controllers.wave_manager import WaveManager
from src.controllers.audio_controller import AudioManager
from src.models.settings import MAP_IMG


class LevelManager:
    """
    Manages game levels including enemy waves, bosses, map loading,
    and projectiles.
    """

    def __init__(self) -> None:
        self.current_level: int = 1
        self.wave_manager: WaveManager = WaveManager(level=self.current_level)
        self.boss_sequence: list[str] = ['ShooterBoss', 'TankBoss', 'SummonerBoss']
        self.boss_index: int = 0
        self.enemies_multiplier: float = 1.0

        self.map_image: Optional[pygame.Surface] = None
        self.collision_mask: Optional[pygame.Mask] = None

        # Sprite groups for enemies, bosses, and projectiles
        self.enemy_group: pygame.sprite.Group = pygame.sprite.Group()
        self.boss_group: pygame.sprite.Group = pygame.sprite.Group()
        self.projectiles: pygame.sprite.Group = pygame.sprite.Group()

    def start_level(self, level: Optional[int] = None) -> None:
        """
        Initializes the level, loads the map and resets enemies, bosses, and projectiles.

        Args:
            level (Optional[int]): Level to start. Defaults to current_level.
        """
        if level is not None:
            self.current_level = level

        self.enemies_multiplier = 1.0 + 0.5 * ((self.current_level - 1) // 3)
        self.wave_manager = WaveManager(level=self.current_level)
        self.wave_manager.start_level()

        groups = self.wave_manager.get_sprite_groups()
        self.enemy_group = groups["enemies"]
        self.boss_group = groups["bosses"]

        self.projectiles.empty()

        map_index = (self.current_level - 1) % len(MAP_IMG)
        map_path = MAP_IMG[map_index]
        self.map_image = pygame.image.load(map_path).convert()
        self.collision_mask = pygame.mask.from_surface(self.map_image)

    def update(self, dt: float) -> None:
        """
        Update projectiles and level state.

        Args:
            dt (float): Delta time since last update.
        """
        self.projectiles.update(dt)

    def on_wave_cleared(self) -> bool:
        """
        Called when a wave is cleared.

        Returns:
            bool: True if all waves cleared and boss should appear, else False.
        """
        if not self.wave_manager.next_wave():
            boss_type = self.get_current_boss_type()
            AudioManager.play_boss_spawn_sfx(boss_type)
            return True
        return False

    def on_boss_defeated(self) -> None:
        """
        Called after the boss is defeated, progresses to next level.
        """
        self.current_level += 1
        self.boss_index = (self.boss_index + 1) % len(self.boss_sequence)
        self.start_level()

    def get_current_boss_type(self) -> str:
        """
        Returns the current boss type string.

        Returns:
            str: Boss type identifier.
        """
        return self.boss_sequence[self.boss_index]

    def get_enemy_count_multiplier(self) -> float:
        """
        Returns the multiplier for enemy count scaling.

        Returns:
            float: Enemy count multiplier.
        """
        return self.enemies_multiplier

    def get_sprite_groups(self) -> Dict[str, pygame.sprite.Group]:
        """
        Returns dictionary of sprite groups.

        Returns:
            Dict[str, pygame.sprite.Group]: Groups for enemies, bosses, and projectiles.
        """
        return {
            "enemies": self.enemy_group,
            "bosses": self.boss_group,
            "projectiles": self.projectiles
        }

    def get_entities(self) -> Dict[str, Any]:
        """
        Returns entities dictionary including boss (if exists).

        Returns:
            Dict[str, Any]: Entities including enemies, boss, projectiles.
        """
        return {
            "enemies": self.enemy_group,
            "boss": self.boss_group.sprites()[0] if self.boss_group else None,
            "projectiles": self.projectiles
        }

    def get_projectile_group(self) -> pygame.sprite.Group:
        """
        Returns the projectiles sprite group.

        Returns:
            pygame.sprite.Group: Group of projectiles.
        """
        return self.projectiles

    def get_map_surface(self) -> Optional[pygame.Surface]:
        """
        Returns the loaded map surface.

        Returns:
            Optional[pygame.Surface]: The map surface image.
        """
        return self.map_image

    def get_collision_mask(self) -> Optional[pygame.Mask]:
        """
        Returns the collision mask generated from the map.

        Returns:
            Optional[pygame.Mask]: Collision mask of the map.
        """
        return self.collision_mask
