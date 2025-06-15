# views/game_view.py

import pygame
from src.models.settings import FONT_PATH


class GameView:
    def __init__(self, screen, tilemap, player, enemies, projectiles, boss=None):
        """
        screen: pygame.Surface - основное окно
        tilemap: TileMap или структура с тайлами уровня
        player: объект Player
        enemies: список врагов
        projectiles: список снарядов
        boss: объект босса (если есть)
        """
        self.screen = screen
        self.tilemap = tilemap
        self.player = player
        self.enemies = enemies
        self.projectiles = projectiles
        self.boss = boss

        self.font = pygame.font.Font(FONT_PATH, 24)
        self.boss_hp_bar_rect = pygame.Rect(20, 20, 300, 25)

    def draw(self):
        self.screen.fill((0, 0, 0))  # фон (черный или другой)

        # Отрисовка карты
        self.draw_map()

        # Отрисовка персонажа
        self.screen.blit(self.player.sprite, self.player.rect)

        # Отрисовка врагов
        for enemy in self.enemies:
            self.screen.blit(enemy.sprite, enemy.rect)

        # Отрисовка снарядов
        for proj in self.projectiles:
            self.screen.blit(proj.sprite, proj.rect)

        # Отрисовка HUD
        self.draw_health()
        if self.boss:
            self.draw_boss_hp()

    def draw_map(self):
        # Предполагается, что tilemap — это 2D массив тайлов
        tile_size = 64  # размер тайла
        for y, row in enumerate(self.tilemap):
            for x, tile in enumerate(row):
                if tile:  # tile — Surface
                    self.screen.blit(tile, (x * tile_size, y * tile_size))

    def draw_health(self):
        # Отрисовка здоровья игрока в виде сердечек или полосы
        health_text = self.font.render(f"Здоровье: {self.player.health}", True, (255, 0, 0))
        self.screen.blit(health_text, (20, self.screen.get_height() - 40))

    def draw_boss_hp(self):
        # Рамка
        pygame.draw.rect(self.screen, (255, 255, 255), self.boss_hp_bar_rect, 2)
        # Заполнение по проценту здоровья босса
        hp_ratio = self.boss.health / self.boss.max_health
        inner_width = int(self.boss_hp_bar_rect.width * hp_ratio)
        inner_rect = pygame.Rect(self.boss_hp_bar_rect.x, self.boss_hp_bar_rect.y, inner_width, self.boss_hp_bar_rect.height)
        pygame.draw.rect(self.screen, (255, 0, 0), inner_rect)

        boss_text = self.font.render("Босс", True, (255, 255, 255))
        self.screen.blit(boss_text, (self.boss_hp_bar_rect.x, self.boss_hp_bar_rect.y - 30))
