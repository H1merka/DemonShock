# models/wave_manager.py

import random
from src.models.enemy import Jumper, Shooter, Warrior, Tank, Summoner
from src.models.settings import WAVES_PER_LEVEL, ENEMY_SCALE_FACTOR
from src.controllers.audio_controller import AudioManager


class WaveManager:
    def __init__(self, level=1):
        self.level = level
        self.waves_per_level = WAVES_PER_LEVEL  # 5 волн на уровень — по типу врагов
        self.current_wave = 0
        self.enemies_to_spawn = []
        self.active_enemies = []

        # Количество врагов растёт на 1.5 раза каждые 3 уровня
        self.base_enemy_count = 5

    def start_level(self):
        self.current_wave = 0
        self.prepare_wave()

    def prepare_wave(self):
        # Определяем тип врага для волны по индексу волны
        enemy_type = self.get_enemy_type_for_wave(self.current_wave)
        enemy_count = self.calculate_enemy_count()

        # Создаём список врагов для спавна
        self.enemies_to_spawn = [self.create_enemy(enemy_type) for _ in range(enemy_count)]
        self.active_enemies = []

    def get_enemy_type_for_wave(self, wave_idx):
        # 0: Jumper, 1: Shooter, 2: Warrior, 3: Tank, 4: Summoner
        enemy_classes = [Jumper, Shooter, Warrior, Tank, Summoner]
        return enemy_classes[wave_idx % len(enemy_classes)]

    def calculate_enemy_count(self):
        # Увеличение врагов каждые 3 уровня
        multiplier = ENEMY_SCALE_FACTOR * ((self.level - 1) // 3)
        return int(self.base_enemy_count * multiplier)

    def create_enemy(self, enemy_class):
        # Создаём врага (можно добавить рандомизацию позиции и параметры)
        # Позиции для спавна можно задавать снаружи, здесь пока (0,0)
        enemy = enemy_class(x=0, y=0)  # координаты позже обновим
        return enemy

    def spawn_next_enemy(self):
        if self.enemies_to_spawn:
            enemy = self.enemies_to_spawn.pop(0)
            # Можно задать случайную позицию в зоне спавна
            enemy.rect.x, enemy.rect.y = self.get_spawn_position()
            self.active_enemies.append(enemy)

            # Воспроизводим звук появления в зависимости от класса
            enemy_type = type(enemy).__name__.lower()  # Пример: "jumper"
            AudioManager.play_enemy_spawn_sfx(enemy_type)

            return enemy
        return None

    def get_spawn_position(self):
        # Возвращаем позицию спавна врага (зависит от уровня карты)
        # Пока простой пример — случайные координаты в пределах экрана
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        return x, y

    def update(self):
        # Вызывается в игровом цикле, например, для спавна врагов постепенно
        # Можно реализовать задержку между спавнами (зависит от нужд)
        pass

    def wave_cleared(self):
        # Волна считается пройденной, если нет активных врагов и нет врагов для спавна
        return not self.active_enemies and not self.enemies_to_spawn

    def next_wave(self):
        if self.current_wave < self.waves_per_level - 1:
            self.current_wave += 1
            self.prepare_wave()
            return True
        else:
            # Все волны уровня пройдены
            return False

    def next_level(self):
        self.level += 1
        self.start_level()
