# controllers/level_manager.py

from src.controllers.wave_manager import WaveManager
from src.controllers.audio_controller import AudioManager


class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.wave_manager = WaveManager(level=self.current_level)
        self.boss_sequence = ['ShooterBoss', 'TankBoss', 'SummonerBoss']
        self.boss_index = 0
        self.enemies_multiplier = 1.0

    def start_level(self):
        self.enemies_multiplier = 1.0 + 0.5 * ((self.current_level - 1) // 3)
        self.wave_manager = WaveManager(level=self.current_level)
        self.wave_manager.start_level()

    def update(self):
        # Здесь можно обновлять состояние уровня, проверять переходы
        pass

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
