import pygame
from src.models.settings import FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT


class GameView:
    def __init__(self, screen, map, player, enemies, projectiles, boss=None):
        """
        screen: pygame.Surface - основное окно
        tilemap: TileMap или структура с тайлами уровня
        player: объект Player
        enemies: список врагов
        projectiles: список снарядов
        boss: объект босса (если есть)
        """
        self.screen = screen
        self.map = map
        self.player = player
        self.enemies = enemies
        self.projectiles = projectiles
        self.boss = boss

        self.font = pygame.font.Font(FONT_PATH, 24)
        self.boss_hp_bar_rect = pygame.Rect(20, 20, 300, 25)
        self.camera_offset = pygame.Vector2(0, 0)

        # Размеры карты
        self.map_width = self.map.get_width()
        self.map_height = self.map.get_height()

    def draw(self):
        self.screen.fill((0, 0, 0))  # фон (черный или другой)

        # === Обновление смещения камеры ===
        self.camera_offset.x = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_offset.y = self.player.rect.centery - SCREEN_HEIGHT // 2

        # Ограничиваем камеру, чтобы не показывать область за пределами карты
        self.camera_offset.x = max(0, min(self.camera_offset.x, self.map_width - SCREEN_WIDTH))
        self.camera_offset.y = max(0, min(self.camera_offset.y, self.map_height - SCREEN_HEIGHT))

        self.draw_map()

        # Игрок
        player_pos = self.player.rect.topleft - self.camera_offset
        self.screen.blit(self.player.image, player_pos)

        # Враги
        for enemy in self.enemies:
            enemy_pos = enemy.rect.topleft - self.camera_offset
            self.screen.blit(enemy.image, enemy_pos)

        # Снаряды
        for proj in self.projectiles:
            proj_pos = proj.rect.topleft - self.camera_offset
            self.screen.blit(proj.image, proj_pos)

        self.draw_health()
        if self.boss:
            self.draw_boss_hp()

    def draw_map(self):
        self.screen.blit(self.map, (-self.camera_offset.x, -self.camera_offset.y))

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

    def update_map_image(self, new_map):
        self.map = new_map
        self.map_width = self.map.get_width()
        self.map_height = self.map.get_height()
