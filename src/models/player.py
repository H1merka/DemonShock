import pygame
from src.models.settings import PLAYER_SPEED, PLAYER_HEALTH, SPRITE_DIR
from src.models.weapon import Pistol, Rifle, AssaultRifle, PlasmaRifle, GrenadeLauncher
from src.controllers.audio_controller import AudioManager


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(SPRITE_DIR + "/player.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.weapon = Pistol()
        self.last_shot_time = 0
        self.shot_cooldown = self.weapon.cooldown
        self.is_moving = False

        self.collision_mask = None  # маска коллизий карты
        self.collision_surface = None  # поверхность карты (для отладки)

    def set_collision_mask(self, surface_or_mask):
        """Устанавливает маску коллизий на основе поверхности или маски"""
        if isinstance(surface_or_mask, pygame.Surface):
            self.collision_mask = pygame.mask.from_threshold(surface_or_mask, (0, 0, 0), (10, 10, 10))
            self.collision_surface = surface_or_mask
        elif isinstance(surface_or_mask, pygame.Mask):
            self.collision_mask = surface_or_mask

    def update(self, movement_vector, dt):
        self.handle_movement(movement_vector, dt)

    def handle_movement(self, movement_vector, dt):
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

    def collides_with_map(self, rect):
        if self.collision_mask is None:
            return False
        offset = (int(rect.left), int(rect.top))
        player_mask = pygame.mask.from_surface(self.image)
        return self.collision_mask.overlap(player_mask, offset) is not None

    def shoot(self, target_pos, current_time, projectiles_group):
        if current_time - self.last_shot_time >= self.weapon.cooldown:
            self.weapon.fire(self.rect.center, target_pos, projectiles_group)
            self.last_shot_time = current_time

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.on_death()

    def on_death(self):
        print("Игрок погиб")

    def switch_weapon(self, weapon_name):
        weapon_classes = {
            "Pistol": Pistol,
            "Rifle": Rifle,
            "AssaultRifle": AssaultRifle,
            "PlasmaRifle": PlasmaRifle,
            "GrenadeLauncher": GrenadeLauncher
        }
        if weapon_name in weapon_classes:
            self.weapon = weapon_classes[weapon_name]()
