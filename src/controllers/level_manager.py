import pygame
from src.controllers.wave_manager import WaveManager
from src.controllers.audio_controller import AudioManager
from src.models.settings import MAP_IMG


class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.wave_manager = WaveManager(level=self.current_level)
        self.boss_sequence = ['ShooterBoss', 'TankBoss', 'SummonerBoss']
        self.boss_index = 0
        self.enemies_multiplier = 1.0

        self.map_image = None
        self.collision_mask = None

        # Группы для отрисовки и обработки
        self.enemy_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

    def start_level(self, level=None):
        if level is not None:
            self.current_level = level

        self.enemies_multiplier = 1.0 + 0.5 * ((self.current_level - 1) // 3)
        self.wave_manager = WaveManager(level=self.current_level)
        self.wave_manager.start_level()

        # Получаем группы спрайтов из wave_manager
        groups = self.wave_manager.get_sprite_groups()
        self.enemy_group = groups["enemies"]
        self.boss_group = groups["bosses"]

        self.projectiles.empty()

        map_index = (self.current_level - 1) % len(MAP_IMG)
        map_path = MAP_IMG[map_index]
        self.map_image = pygame.image.load(map_path).convert()
        self.collision_mask = pygame.mask.from_surface(self.map_image)

    def update(self, dt):
        # Здесь можно обновлять состояние уровня, проверять переходы
        self.projectiles.update(dt)

    def on_wave_cleared(self):
        """Вызывается, когда волна очищена"""
        if not self.wave_manager.next_wave():
            # Все волны пройдены — появляется босс
            boss_type = self.get_current_boss_type()
            AudioManager.play_boss_spawn_sfx(boss_type)  # Проигрываем звук
            return True  # сигнал к появлению босса
        return False

    def on_boss_defeated(self):
        """Вызывается после победы над боссом"""
        self.current_level += 1
        self.boss_index = (self.boss_index + 1) % len(self.boss_sequence)
        self.start_level()

    def get_current_boss_type(self):
        return self.boss_sequence[self.boss_index]

    def get_enemy_count_multiplier(self):
        return self.enemies_multiplier

    def get_sprite_groups(self):
        return {
            "enemies": self.enemy_group,
            "bosses": self.boss_group,
            "projectiles": self.projectiles
        }

    def get_entities(self):
        return {
            "enemies": self.enemy_group,
            "boss": self.boss_group.sprites()[0] if self.boss_group else None,
            "projectiles": self.projectiles
        }

    def get_projectile_group(self):
        return self.projectiles

    def get_map_surface(self):
        return self.map_image

    def get_collision_mask(self):
        return self.collision_mask
