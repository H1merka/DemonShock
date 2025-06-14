# models/enemy.py

import pygame
import random
from settings import TILE_SIZE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, health, speed, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.health = health
        self.speed = speed

    def update(self, player_pos, dt):
        # Простейшее движение к игроку
        direction = pygame.Vector2(player_pos) - self.pos
        if direction.length() != 0:
            self.pos += direction.normalize() * self.speed * dt
            self.rect.center = self.pos

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()


# === Обычные враги ===

class Jumper(Enemy):
    def __init__(self, pos):
        super().__init__(pos, health=2, speed=250, image_path="assets/sprites/enemies/jumper.png")

class Shooter(Enemy):
    def __init__(self, pos):
        super().__init__(pos, health=2, speed=120, image_path="assets/sprites/enemies/shooter.png")
        self.shoot_timer = 0

    def update(self, player_pos, dt):
        super().update(player_pos, dt)
        self.shoot_timer += dt
        if self.shoot_timer >= 2000:
            self.shoot_timer = 0
            # Логика выстрела в игрока
            # Вызывается из GameController — отслеживает врагов с типом Shooter

class Warrior(Enemy):
    def __init__(self, pos):
        super().__init__(pos, health=2, speed=180, image_path="assets/sprites/enemies/warrior.png")

class Tank(Enemy):
    def __init__(self, pos):
        super().__init__(pos, health=4, speed=80, image_path="assets/sprites/enemies/tank.png")

class Summoner(Enemy):
    def __init__(self, pos):
        super().__init__(pos, health=2, speed=100, image_path="assets/sprites/enemies/summoner.png")
        self.summon_timer = 0

    def update(self, player_pos, dt):
        super().update(player_pos, dt)
        self.summon_timer += dt
        if self.summon_timer >= 3000:
            self.summon_timer = 0
            # Призывает 1–2 прыгуна
            return True  # Сигнал для контроллера на призыв
        return False


# === Боссы ===

class Boss(Enemy):
    def __init__(self, pos, image_path):
        super().__init__(pos, health=100, speed=60, image_path=image_path)

class BossShooter(Boss):
    def __init__(self, pos):
        super().__init__(pos, image_path="assets/sprites/bosses/boss_shooter.png")
        self.shoot_timer = 0

    def update(self, player_pos, dt):
        super().update(player_pos, dt)
        self.shoot_timer += dt
        if self.shoot_timer >= 1000:
            self.shoot_timer = 0
            return "shoot"  # Сигнал для GameController
        return None

class BossTank(Boss):
    def __init__(self, pos):
        super().__init__(pos, image_path="assets/sprites/bosses/boss_tank.png")

class BossSummoner(Boss):
    def __init__(self, pos):
        super().__init__(pos, image_path="assets/sprites/bosses/boss_summoner.png")
        self.summon_timer = 0

    def update(self, player_pos, dt):
        super().update(player_pos, dt)
        self.summon_timer += dt
        if self.summon_timer >= 2500:
            self.summon_timer = 0
            return "summon"
        return None
