import pygame
from typing import Optional, Union
from src.models.settings import ENEMY_HEALTH, BOSS_HEALTH, SPRITE_DIR
import os


class Enemy(pygame.sprite.Sprite):
    """
    Base class for enemies.

    Attributes:
        pos (pygame.Vector2): Current position.
        health (int): Current health points.
        speed (float): Movement speed.
        image (pygame.Surface): Enemy sprite image.
        rect (pygame.Rect): Rectangle for positioning and collisions.
    """

    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2], health: int, speed: float, image_path: str) -> None:
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.health = health
        self.speed = speed

    def update(self, player_pos: Union[tuple[float, float], pygame.Vector2], dt: float) -> None:
        """
        Move enemy towards the player position.

        Args:
            player_pos (tuple[float, float] | pygame.Vector2): Player's current position.
            dt (float): Delta time since last update (seconds).
        """
        direction = pygame.Vector2(player_pos) - self.pos
        if direction.length() != 0:
            self.pos += direction.normalize() * self.speed * dt
            self.rect.center = self.pos

    def take_damage(self, amount: int) -> None:
        """
        Reduce health by damage amount and kill sprite if health falls to zero or below.

        Args:
            amount (int): Damage to apply.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()


# === Regular Enemies ===

class Jumper(Enemy):
    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, health=ENEMY_HEALTH, speed=250, image_path=os.path.join(SPRITE_DIR, "enemies", "jumper.png"))


class Shooter(Enemy):
    """
    Enemy that can shoot at the player.
    """

    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, health=ENEMY_HEALTH, speed=120, image_path=os.path.join(SPRITE_DIR, "enemies", "shooter.png"))
        self.shoot_timer: float = 0

    def update(self, player_pos: Union[tuple[float, float], pygame.Vector2], dt: float) -> None:
        """
        Update movement and shooting timer.

        Note:
            Shooting logic is handled externally (e.g. GameController).

        Args:
            player_pos (tuple[float, float] | pygame.Vector2): Player's position.
            dt (float): Delta time in seconds.
        """
        super().update(player_pos, dt)
        self.shoot_timer += dt
        if self.shoot_timer >= 2000:
            self.shoot_timer = 0
            # Shooting action triggered externally


class Warrior(Enemy):
    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, health=ENEMY_HEALTH, speed=180, image_path=os.path.join(SPRITE_DIR, "enemies", "warrior.png"))


class Tank(Enemy):
    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, health=(ENEMY_HEALTH * 2), speed=80, image_path=os.path.join(SPRITE_DIR, "enemies", "tank.png"))


class Summoner(Enemy):
    """
    Enemy that periodically summons additional enemies.
    """

    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, health=ENEMY_HEALTH, speed=100, image_path=os.path.join(SPRITE_DIR, "enemies", "summoner.png"))
        self.summon_timer: float = 0

    def update(self, player_pos: Union[tuple[float, float], pygame.Vector2], dt: float) -> bool:
        """
        Update movement and summon timer.

        Args:
            player_pos (tuple[float, float] | pygame.Vector2): Player's position.
            dt (float): Delta time in seconds.

        Returns:
            bool: True if summon event triggered, else False.
        """
        super().update(player_pos, dt)
        self.summon_timer += dt
        if self.summon_timer >= 3000:
            self.summon_timer = 0
            return True
        return False


# === Bosses ===

class Boss(Enemy):
    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2], image_path: str) -> None:
        super().__init__(pos, health=BOSS_HEALTH, speed=60, image_path=image_path)


class BossShooter(Boss):
    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, image_path=os.path.join(SPRITE_DIR, "bosses", "boss_shooter.png"))
        self.shoot_timer: float = 0

    def update(self, player_pos: Union[tuple[float, float], pygame.Vector2], dt: float) -> Optional[str]:
        """
        Update movement and shooting timer.

        Args:
            player_pos (tuple[float, float] | pygame.Vector2): Player's position.
            dt (float): Delta time in seconds.

        Returns:
            Optional[str]: "shoot" if shooting event triggered, else None.
        """
        super().update(player_pos, dt)
        self.shoot_timer += dt
        if self.shoot_timer >= 1000:
            self.shoot_timer = 0
            return "shoot"
        return None


class BossTank(Boss):
    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, image_path=os.path.join(SPRITE_DIR, "bosses", "boss_tank.png"))


class BossSummoner(Boss):
    def __init__(self, pos: Union[tuple[float, float], pygame.Vector2]) -> None:
        super().__init__(pos, image_path=os.path.join(SPRITE_DIR, "bosses", "boss_summoner.png"))
        self.summon_timer: float = 0

    def update(self, player_pos: Union[tuple[float, float], pygame.Vector2], dt: float) -> Optional[str]:
        """
        Update movement and summon timer.

        Args:
            player_pos (tuple[float, float] | pygame.Vector2): Player's position.
            dt (float): Delta time in seconds.

        Returns:
            Optional[str]: "summon" if summon event triggered, else None.
        """
        super().update(player_pos, dt)
        self.summon_timer += dt
        if self.summon_timer >= 2500:
            self.summon_timer = 0
            return "summon"
        return None
