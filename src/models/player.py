import pygame
from typing import Optional, Tuple, Union
from src.models.settings import PLAYER_SPEED, PLAYER_HEALTH, SPRITE_DIR
from src.models.weapon import Pistol, Rifle, AssaultRifle, PlasmaRifle, GrenadeLauncher
from src.controllers.audio_controller import AudioManager


class Player(pygame.sprite.Sprite):
    """
    Player character controlled by the user.

    Attributes:
        WEAPON_CLASSES (dict): Mapping of weapon names to their classes.
        image (pygame.Surface): Player sprite image.
        rect (pygame.Rect): Rectangle for positioning and collisions.
        speed (float): Player movement speed.
        health (int): Player health points.
        weapon (Weapon): Currently equipped weapon.
        last_shot_time (int): Time of last shot in milliseconds.
        shot_cooldown (int): Cooldown time between shots in milliseconds.
        is_moving (bool): Whether the player is currently moving.
        collision_mask (Optional[pygame.Mask]): Mask used for map collision detection.
        collision_surface (Optional[pygame.Surface]): Surface for collision mask debugging.
    """

    WEAPON_CLASSES = {
        "Pistol": Pistol,
        "Rifle": Rifle,
        "AssaultRifle": AssaultRifle,
        "PlasmaRifle": PlasmaRifle,
        "GrenadeLauncher": GrenadeLauncher
    }

    def __init__(self, pos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.image.load(f"{SPRITE_DIR}/player.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.speed: float = PLAYER_SPEED
        self.health: int = PLAYER_HEALTH
        self.weapon = Pistol()
        self.last_shot_time: int = 0
        self.shot_cooldown: int = self.weapon.cooldown
        self.is_moving: bool = False

        self.collision_mask: Optional[pygame.Mask] = None
        self.collision_surface: Optional[pygame.Surface] = None

    def set_collision_mask(self, surface_or_mask: Union[pygame.Surface, pygame.Mask]) -> None:
        """
        Set the collision mask for the player using either a surface or a mask.

        Args:
            surface_or_mask (Union[pygame.Surface, pygame.Mask]): Surface or mask to create collision mask from.
        """
        if isinstance(surface_or_mask, pygame.Surface):
            self.collision_mask = pygame.mask.from_threshold(surface_or_mask, (0, 0, 0), (10, 10, 10))
            self.collision_surface = surface_or_mask
        elif isinstance(surface_or_mask, pygame.Mask):
            self.collision_mask = surface_or_mask

    def update(self, movement_vector: Tuple[float, float], dt: float) -> None:
        """
        Update the player's state, including movement.

        Args:
            movement_vector (Tuple[float, float]): Movement direction vector (dx, dy).
            dt (float): Time delta in seconds since last update.
        """
        self.handle_movement(movement_vector, dt)

    def handle_movement(self, movement_vector: Tuple[float, float], dt: float) -> None:
        """
        Handle player movement with collision checking.

        Args:
            movement_vector (Tuple[float, float]): Movement direction vector (dx, dy).
            dt (float): Time delta in seconds since last update.
        """
        dx, dy = movement_vector

        is_now_moving = dx != 0 or dy != 0

        if is_now_moving and not self.is_moving:
            AudioManager.play_step_sfx()
        elif not is_now_moving and self.is_moving:
            AudioManager.stop_step_sfx()

        self.is_moving = is_now_moving

        if dx == 0 and dy == 0:
            return

        new_rect = self.rect.copy()
        new_rect.x += dx * self.speed * dt
        if not self.collides_with_map(new_rect):
            self.rect.x = new_rect.x

        new_rect.y += dy * self.speed * dt
        if not self.collides_with_map(new_rect):
            self.rect.y = new_rect.y

    def collides_with_map(self, rect: pygame.Rect) -> bool:
        """
        Check if the player collides with the map collision mask.

        Args:
            rect (pygame.Rect): Rectangle to check collision for.

        Returns:
            bool: True if colliding with map, False otherwise.
        """
        if self.collision_mask is None:
            return False
        offset = (int(rect.left), int(rect.top))
        player_mask = pygame.mask.from_surface(self.image)
        return self.collision_mask.overlap(player_mask, offset) is not None

    def shoot(self, target_pos: Tuple[int, int], current_time: int, projectiles_group: pygame.sprite.Group) -> None:
        """
        Fire the currently equipped weapon if cooldown allows.

        Args:
            target_pos (Tuple[int, int]): Target position to shoot at.
            current_time (int): Current time in milliseconds.
            projectiles_group (pygame.sprite.Group): Group to add new projectiles to.
        """
        if current_time - self.last_shot_time >= self.weapon.cooldown:
            self.weapon.fire(self.rect.center, target_pos, projectiles_group)
            self.last_shot_time = current_time

    def take_damage(self, amount: int) -> None:
        """
        Reduce player's health by the given amount and handle death.

        Args:
            amount (int): Damage amount to apply.
        """
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.on_death()

    def on_death(self) -> None:
        """Handle player death event."""
        print("Player has died")

    def switch_weapon(self, weapon_name: str) -> None:
        """
        Switch the current weapon by its name.

        Args:
            weapon_name (str): Name of the weapon to switch to.
        """
        if weapon_name in self.WEAPON_CLASSES:
            self.weapon = self.WEAPON_CLASSES[weapon_name]()
