# models/projectile.py

import pygame
import os
from src.models.settings import WEAPON_DAMAGE, WEAPON_SPRITES_DIR


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, speed, damage, image_path):
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

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = self.pos

        # Удаление, если за пределами экрана
        screen_rect = pygame.Rect(0, 0, 1280, 720)
        if not screen_rect.colliderect(self.rect):
            self.kill()

# === Классы снарядов ===


class Bullet(Projectile):
    def __init__(self, pos, target_pos):
        super().__init__(pos, target_pos, speed=600, damage=WEAPON_DAMAGE["Pistol"], image_path=os.path.join(WEAPON_SPRITES_DIR, "bullet.png"))


class RifleBullet(Projectile):
    def __init__(self, pos, target_pos):
        super().__init__(pos, target_pos, speed=800, damage=WEAPON_DAMAGE["Rifle"], image_path=os.path.join(WEAPON_SPRITES_DIR, "bullet.png"))


class PlasmaBolt(Projectile):
    def __init__(self, pos, target_pos):
        super().__init__(pos, target_pos, speed=500, damage=WEAPON_DAMAGE["PlasmaRifle"], image_path=os.path.join(WEAPON_SPRITES_DIR, "plasma_bolt.png"))


class Grenade(Projectile):
    def __init__(self, pos, target_pos):
        super().__init__(pos, target_pos, speed=400, damage=WEAPON_DAMAGE["GrenadeLauncher"], image_path=os.path.join(WEAPON_SPRITES_DIR, "grenade.png"))

    def update(self, dt):
        super().update(dt)
        # В будущем: реализовать взрыв по таймеру или столкновению

# === Вспомогательная функция ===


def create_projectile(weapon_name, pos, target_pos):
    if weapon_name == "Pistol":
        return Bullet(pos, target_pos)
    elif weapon_name == "Rifle":
        return RifleBullet(pos, target_pos)
    elif weapon_name == "PlasmaRifle":
        return PlasmaBolt(pos, target_pos)
    elif weapon_name == "GrenadeLauncher":
        return Grenade(pos, target_pos)
    elif weapon_name == "AssaultRifle":
        return Bullet(pos, target_pos)  # та же пуля, но стрельба очередями
    return None
