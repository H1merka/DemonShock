import pygame
from typing import Tuple
from src.models.projectile import create_projectile
from src.models.settings import WEAPON_SPRITES_DIR
from src.controllers.audio_controller import AudioManager


class Weapon:
    """
    Base class for weapons.

    Attributes:
        name (str): Weapon name.
        damage (int): Damage dealt per shot.
        cooldown (int): Cooldown time in milliseconds.
        projectile_type (str): Type of projectile this weapon fires.
        icon (pygame.Surface): Weapon icon image.
    """

    def __init__(self, name: str, damage: int, cooldown: int, projectile_type: str) -> None:
        self.name = name
        self.damage = damage
        self.cooldown = cooldown  # cooldown in milliseconds
        self.projectile_type = projectile_type
        self.icon = pygame.image.load(f"{WEAPON_SPRITES_DIR}/{name.lower()}_icon.png").convert_alpha()

    def fire(self, start_pos: Tuple[int, int], target_pos: Tuple[int, int], projectiles_group: pygame.sprite.Group) -> None:
        """
        Fire a projectile from start_pos towards target_pos and add it to the projectiles group.

        Args:
            start_pos (Tuple[int, int]): Starting position of the projectile.
            target_pos (Tuple[int, int]): Target position to aim at.
            projectiles_group (pygame.sprite.Group): Group to which the new projectile will be added.
        """
        projectile = create_projectile(self.name, start_pos, target_pos)
        if projectile:
            projectiles_group.add(projectile)
            AudioManager.play_weapon_sfx(self.name)


class Pistol(Weapon):
    def __init__(self) -> None:
        super().__init__(name="Pistol", damage=1, cooldown=400, projectile_type="Bullet")


class Rifle(Weapon):
    def __init__(self) -> None:
        super().__init__(name="Rifle", damage=3, cooldown=700, projectile_type="RifleBullet")


class AssaultRifle(Weapon):
    """
    Assault rifle that fires bursts of bullets with a small spread.
    """

    def __init__(self) -> None:
        super().__init__(name="AssaultRifle", damage=1, cooldown=150, projectile_type="Bullet")
        self.shots_per_burst = 3

    def fire(self, start_pos: Tuple[int, int], target_pos: Tuple[int, int], projectiles_group: pygame.sprite.Group) -> None:
        """
        Fire multiple projectiles in a burst with slight position offsets for spread.

        Args:
            start_pos (Tuple[int, int]): Starting position of the projectiles.
            target_pos (Tuple[int, int]): Target position to aim at.
            projectiles_group (pygame.sprite.Group): Group to which the new projectiles will be added.
        """
        for i in range(self.shots_per_burst):
            projectile = create_projectile(self.name, start_pos, target_pos)
            if projectile:
                # Slight positional offset to simulate spread
                projectile.rect.x += i * 2
                projectile.rect.y += i * 2
                projectiles_group.add(projectile)
        AudioManager.play_weapon_sfx(self.name)


class PlasmaRifle(Weapon):
    def __init__(self) -> None:
        super().__init__(name="PlasmaRifle", damage=4, cooldown=600, projectile_type="PlasmaBolt")


class GrenadeLauncher(Weapon):
    def __init__(self) -> None:
        super().__init__(name="GrenadeLauncher", damage=5, cooldown=1000, projectile_type="Grenade")
