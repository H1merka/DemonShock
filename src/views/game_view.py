import pygame
from typing import Optional, List, Union
from src.models.settings import FONT_PATH


class GameView:
    """
    Handles all drawing operations of the game including map, entities, and UI.

    Attributes:
        screen (pygame.Surface): The main game window surface.
        map (pygame.Surface): Tilemap or surface representing the game level.
        player (pygame.sprite.Sprite): Player object.
        enemies (List[pygame.sprite.Sprite]): List of enemy objects.
        projectiles (List[pygame.sprite.Sprite]): List of projectile objects.
        boss (Optional[pygame.sprite.Sprite]): Boss object if present.
        font (pygame.font.Font): Font for rendering UI text.
        boss_hp_bar_rect (pygame.Rect): Rectangle defining boss health bar position and size.
        camera_offset (pygame.Vector2): Offset for camera scrolling.
        screen_width (int): Width of the game screen.
        screen_height (int): Height of the game screen.
        map_width (int): Width of the level map.
        map_height (int): Height of the level map.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        map: pygame.Surface,
        player: pygame.sprite.Sprite,
        enemies: List[pygame.sprite.Sprite],
        projectiles: List[pygame.sprite.Sprite],
        boss: Optional[pygame.sprite.Sprite] = None,
    ) -> None:
        self.screen = screen
        self.map = map
        self.player = player
        self.enemies = enemies
        self.projectiles = projectiles
        self.boss = boss

        self.font = pygame.font.Font(FONT_PATH, 24)
        self.boss_hp_bar_rect = pygame.Rect(20, 20, 300, 25)
        self.camera_offset = pygame.Vector2(0, 0)

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.map_width = self.map.get_width()
        self.map_height = self.map.get_height()

    def draw(self) -> None:
        """
        Draw the entire game scene including map, entities, and UI.
        """
        self.screen.fill((0, 0, 0))
        self.update_camera()

        self.draw_map()
        self.draw_entities()
        self.draw_ui()

    def update_camera(self) -> None:
        """
        Update the camera offset based on the player's position,
        clamping it within the map bounds.
        """
        self.camera_offset.x = self.player.rect.centerx - self.screen_width // 2
        self.camera_offset.y = self.player.rect.centery - self.screen_height // 2

        self.camera_offset.x = max(0, min(self.camera_offset.x, self.map_width - self.screen_width))
        self.camera_offset.y = max(0, min(self.camera_offset.y, self.map_height - self.screen_height))

    def draw_map(self) -> None:
        """
        Draw the level map on the screen with camera offset applied.
        """
        self.screen.blit(self.map, (-self.camera_offset.x, -self.camera_offset.y))

    def draw_entities(self) -> None:
        """
        Draw player, enemies, and projectiles on the screen
        with camera offset applied.
        """
        self.screen.blit(self.player.image, self.player.rect.topleft - self.camera_offset)

        for enemy in self.enemies:
            self.screen.blit(enemy.image, enemy.rect.topleft - self.camera_offset)

        for proj in self.projectiles:
            self.screen.blit(proj.image, proj.rect.topleft - self.camera_offset)

    def draw_ui(self) -> None:
        """
        Draw UI elements such as player health and boss health bar.
        """
        self.draw_health()
        if self.boss:
            self.draw_boss_hp()

    def draw_health(self) -> None:
        """
        Draw player's health on the screen as text.
        """
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 0, 0))
        self.screen.blit(health_text, (20, self.screen.get_height() - 40))

    def draw_boss_hp(self) -> None:
        """
        Draw the boss health bar with current health ratio.
        """
        pygame.draw.rect(self.screen, (255, 255, 255), self.boss_hp_bar_rect, 2)
        hp_ratio = self.boss.health / self.boss.max_health
        inner_width = int(self.boss_hp_bar_rect.width * hp_ratio)
        inner_rect = pygame.Rect(
            self.boss_hp_bar_rect.x,
            self.boss_hp_bar_rect.y,
            inner_width,
            self.boss_hp_bar_rect.height,
        )
        pygame.draw.rect(self.screen, (255, 0, 0), inner_rect)

        boss_text = self.font.render("Boss", True, (255, 255, 255))
        self.screen.blit(boss_text, (self.boss_hp_bar_rect.x, self.boss_hp_bar_rect.y - 30))

    def update_map_image(self, new_map: pygame.Surface) -> None:
        """
        Update the level map surface and dimensions.

        Args:
            new_map (pygame.Surface): New tilemap or level surface.
        """
        self.map = new_map
        self.map_width = self.map.get_width()
        self.map_height = self.map.get_height()
