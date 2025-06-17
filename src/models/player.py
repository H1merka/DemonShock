# models/player.py

import pygame
from src.models.settings import PLAYER_SPEED, PLAYER_HEALTH, SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_DIR
from src.models.weapon import Pistol, Rifle, AssaultRifle, PlasmaRifle, GrenadeLauncher
from src.controllers.audio_controller import AudioManager


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(SPRITE_DIR + "player.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.weapon = Pistol()
        self.last_shot_time = 0
        self.shot_cooldown = self.weapon.cooldown
        self.is_moving = False

    def update(self, keys_pressed, dt):
        self.handle_movement(keys_pressed, dt)

    def handle_movement(self, keys, dt):
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        is_now_moving = dx != 0 or dy != 0

        if is_now_moving and not self.is_moving:
            AudioManager.play_step_sfx()
        elif not is_now_moving and self.is_moving:
            AudioManager.stop_step_sfx()

        self.is_moving = is_now_moving

        self.rect.x += dx * dt
        self.rect.y += dy * dt

        # Ограничения экрана
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

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
