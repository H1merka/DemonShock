import pygame
import os
from typing import Optional
from src.models.settings import WEAPON_DAMAGE, WEAPON_SPRITES_DIR


class Projectile(pygame.sprite.Sprite):
    """
    Base class for projectiles fired by weapons.

    Attributes:
        pos (pygame.Vector2): Current position of the projectile.
        target (pygame.Vector2): Target position for the projectile.
        speed (float): Movement speed of the projectile.
        damage (int): Damage dealt by the projectile.
        velocity (pygame.Vector2): Normalized velocity vector scaled by speed.
    """

    def __init__(self, pos: tuple[float, float], target_pos: tuple[float, float], speed: float, damage: int, image_path: str) -> None:
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.target = pygame.Vector2(target_pos)
        self.speed = speed
        self.damage = damage

        direction = self.target - self.pos
        if direction.length() != 0:
            self.velocity = direction.normalize() * speed
        else:
            self.velocity = pygame.Vector2(0, 0)

    def update(self, dt: float) -> None:
        """
        Update projectile position and remove it if it goes outside the screen bounds.

        Args:
            dt (float): Delta time since last frame in seconds.
        """
        self.pos += self.velocity * dt
        self.rect.center = self.pos

        screen_rect = pygame.Rect(0, 0, 1280, 720)
        if not screen_rect.colliderect(self.rect):
            self.kill()


class Bullet(Projectile):
    """Projectile subclass representing a pistol bullet."""

    def __init__(self, pos: tuple[float, float], target_pos: tuple[float, float]) -> None:
        super().__init__(
            pos,
            target_pos,
            speed=600,
            damage=WEAPON_DAMAGE["Pistol"],
            image_path=os.path.join(WEAPON_SPRITES_DIR, "bullet.png")
        )


class RifleBullet(Projectile):
    """Projectile subclass representing a rifle bullet."""

    def __init__(self, pos: tuple[float, float], target_pos: tuple[float, float]) -> None:
        super().__init__(
            pos,
            target_pos,
            speed=800,
            damage=WEAPON_DAMAGE["Rifle"],
            image_path=os.path.join(WEAPON_SPRITES_DIR, "bullet.png")
        )


class PlasmaBolt(Projectile):
    """Projectile subclass representing a plasma rifle bolt."""

    def __init__(self, pos: tuple[float, float], target_pos: tuple[float, float]) -> None:
        super().__init__(
            pos,
            target_pos,
            speed=500,
            damage=WEAPON_DAMAGE["PlasmaRifle"],
            image_path=os.path.join(WEAPON_SPRITES_DIR, "plasma_bolt.png")
        )


class Grenade(Projectile):
    """Projectile subclass representing a grenade."""

    def __init__(self, pos: tuple[float, float], target_pos: tuple[float, float]) -> None:
        super().__init__(
            pos,
            target_pos,
            speed=400,
            damage=WEAPON_DAMAGE["GrenadeLauncher"],
            image_path=os.path.join(WEAPON_SPRITES_DIR, "grenade.png")
        )

    def update(self, dt: float) -> None:
        """
        Update grenade position.

        Note:
            Future implementation may include timed explosion or collision detection.
        """
        super().update(dt)


def create_projectile(weapon_name: str, pos: tuple[float, float], target_pos: tuple[float, float]) -> Optional[Projectile]:
    """
    Factory function to create a projectile based on weapon name.

    Args:
        weapon_name (str): Name of the weapon.
        pos (tuple[float, float]): Starting position of the projectile.
        target_pos (tuple[float, float]): Target position.

    Returns:
        Optional[Projectile]: Instance of a Projectile subclass or None if unknown weapon.
    """
    if weapon_name == "Pistol":
        return Bullet(pos, target_pos)
    elif weapon_name == "Rifle":
        return RifleBullet(pos, target_pos)
    elif weapon_name == "PlasmaRifle":
        return PlasmaBolt(pos, target_pos)
    elif weapon_name == "GrenadeLauncher":
        return Grenade(pos, target_pos)
    elif weapon_name == "AssaultRifle":
        return Bullet(pos, target_pos)  # Same bullet, but used for burst fire
    return None
