# models/weapon.py

import pygame
from src.models.projectile import create_projectile
from src.models.settings import WEAPON_SPRITES_DIR
from src.controllers.audio_controller import AudioManager


class Weapon:
    def __init__(self, name, damage, cooldown, projectile_type):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown  # в миллисекундах
        self.projectile_type = projectile_type
        self.icon = pygame.image.load(WEAPON_SPRITES_DIR + f"{name.lower()}_icon.png").convert_alpha()

    def fire(self, start_pos, target_pos, projectiles_group):
        projectile = create_projectile(self.name, start_pos, target_pos)
        if projectile:
            projectiles_group.add(projectile)
            AudioManager.play_weapon_sfx(self.name)


class Pistol(Weapon):
    def __init__(self):
        super().__init__(name="Pistol", damage=1, cooldown=400, projectile_type="Bullet")


class Rifle(Weapon):
    def __init__(self):
        super().__init__(name="Rifle", damage=3, cooldown=700, projectile_type="RifleBullet")


class AssaultRifle(Weapon):
    def __init__(self):
        super().__init__(name="AssaultRifle", damage=1, cooldown=150, projectile_type="Bullet")
        self.shots_per_burst = 3

    def fire(self, start_pos, target_pos, projectiles_group):
        for i in range(self.shots_per_burst):
            projectile = create_projectile(self.name, start_pos, target_pos)
            if projectile:
                # Небольшой разброс — добавим случайное смещение
                projectile.rect.x += i * 2
                projectile.rect.y += i * 2
                projectiles_group.add(projectile)
        AudioManager.play_weapon_sfx(self.name)


class PlasmaRifle(Weapon):
    def __init__(self):
        super().__init__(name="PlasmaRifle", damage=4, cooldown=600, projectile_type="PlasmaBolt")


class GrenadeLauncher(Weapon):
    def __init__(self):
        super().__init__(name="GrenadeLauncher", damage=5, cooldown=1000, projectile_type="Grenade")
