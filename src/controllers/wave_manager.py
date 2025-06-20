import pygame
import random
from typing import Optional, Type, Dict, List, Union
from src.models.enemy import Jumper, Shooter, Warrior, Tank, Summoner
from src.models.settings import WAVES_PER_LEVEL, ENEMY_SCALE_FACTOR
from src.controllers.audio_controller import AudioManager


class WaveManager:
    """
    Manages enemy waves for a given level, including spawning and tracking active enemies.
    """

    def __init__(self, level: int = 1) -> None:
        self.level: int = level
        self.waves_per_level: int = WAVES_PER_LEVEL  # Number of waves per level
        self.current_wave: int = 0
        self.enemies_to_spawn: List[pygame.sprite.Sprite] = []
        self.active_enemies: List[pygame.sprite.Sprite] = []

        # Sprite groups for enemies and bosses
        self.enemy_group: pygame.sprite.Group = pygame.sprite.Group()
        self.boss_group: pygame.sprite.Group = pygame.sprite.Group()

        # Base enemy count, grows with level scaling
        self.base_enemy_count: int = 5

    def start_level(self) -> None:
        """
        Initializes the first wave of the current level.
        """
        self.current_wave = 0
        self.prepare_wave()

    def prepare_wave(self) -> None:
        """
        Prepares the list of enemies to spawn for the current wave.
        """
        enemy_type: Type[pygame.sprite.Sprite] = self.get_enemy_type_for_wave(self.current_wave)
        enemy_count: int = self.calculate_enemy_count()

        self.enemies_to_spawn = [self.create_enemy(enemy_type) for _ in range(enemy_count)]
        self.active_enemies = []
        self.enemy_group.empty()

    def get_enemy_type_for_wave(self, wave_idx: int) -> Type[pygame.sprite.Sprite]:
        """
        Returns the enemy class for a given wave index.

        Args:
            wave_idx (int): Index of the wave.

        Returns:
            Type[pygame.sprite.Sprite]: Enemy class type.
        """
        enemy_classes = [Jumper, Shooter, Warrior, Tank, Summoner]
        return enemy_classes[wave_idx % len(enemy_classes)]

    def calculate_enemy_count(self) -> int:
        """
        Calculates the number of enemies to spawn, scaling with level.

        Returns:
            int: Number of enemies to spawn.
        """
        multiplier = ENEMY_SCALE_FACTOR * ((self.level - 1) // 3)
        return int(self.base_enemy_count * multiplier)

    def create_enemy(self, enemy_class: Type[pygame.sprite.Sprite]) -> pygame.sprite.Sprite:
        """
        Creates an enemy instance. Position will be updated later.

        Args:
            enemy_class (Type[pygame.sprite.Sprite]): Enemy class to instantiate.

        Returns:
            pygame.sprite.Sprite: Created enemy instance.
        """
        enemy = enemy_class(x=0, y=0)  # Initial position placeholder
        return enemy

    def spawn_next_enemy(self) -> Optional[pygame.sprite.Sprite]:
        """
        Spawns the next enemy from the spawn queue, placing it at a spawn position.

        Returns:
            Optional[pygame.sprite.Sprite]: The spawned enemy, or None if no enemies left.
        """
        if self.enemies_to_spawn:
            enemy = self.enemies_to_spawn.pop(0)
            enemy.rect.x, enemy.rect.y = self.get_spawn_position()
            self.active_enemies.append(enemy)
            self.enemy_group.add(enemy)

            enemy_type = type(enemy).__name__.lower()  # e.g., "jumper"
            AudioManager.play_enemy_spawn_sfx(enemy_type)

            return enemy
        return None

    def get_spawn_position(self) -> tuple[int, int]:
        """
        Returns a random spawn position for an enemy.

        Returns:
            tuple[int, int]: (x, y) spawn coordinates.
        """
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        return x, y

    def update(self) -> None:
        """
        Update method called each game loop iteration. Can be used for timed spawning or other logic.
        """
        pass

    def wave_cleared(self) -> bool:
        """
        Checks if the current wave has been cleared.

        Returns:
            bool: True if no active enemies and no enemies left to spawn.
        """
        return not self.active_enemies and not self.enemies_to_spawn

    def next_wave(self) -> bool:
        """
        Advances to the next wave if possible.

        Returns:
            bool: True if next wave started, False if no more waves in the level.
        """
        if self.current_wave < self.waves_per_level - 1:
            self.current_wave += 1
            self.prepare_wave()
            return True
        else:
            return False

    def next_level(self) -> None:
        """
        Advances to the next level and resets waves.
        """
        self.level += 1
        self.start_level()

    def get_sprite_groups(self) -> Dict[str, pygame.sprite.Group]:
        """
        Returns dictionary of sprite groups.

        Returns:
            Dict[str, pygame.sprite.Group]: Groups for enemies and bosses.
        """
        return {
            "enemies": self.enemy_group,
            "bosses": self.boss_group
        }
