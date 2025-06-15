# settings.py

import os

# Экран
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Demonic Invasion"

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Игрок
PLAYER_SPEED = 5
PLAYER_HEALTH = 3

# Враги
ENEMY_HEALTH = 2
BOSS_HEALTH = 100
ENEMY_SPAWN_DELAY = 2000  # миллисекунды
BOSS_SPAWN_DELAY = 5000

# Уровни
WAVES_PER_LEVEL = 5
ENEMY_SCALE_FACTOR = 1.5  # увеличение кол-ва врагов каждые 3 уровня

# Пути к ассетам
ASSET_DIR = "assets"
FONT_PATH = os.path.join(ASSET_DIR, "fonts", "russian_font.ttf")
TILESET_DIR = os.path.join(ASSET_DIR, "tilesets")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")
ICON_PATH = os.path.join(ASSET_DIR, "icons", "game_icon.png")
MUSIC_DIR = os.path.join(ASSET_DIR, "music")
SFX_DIR = os.path.join(ASSET_DIR, "sfx")
UI_DIR = os.path.join(ASSET_DIR, "ui")
WEAPON_SPRITES_DIR = os.path.join(ASSET_DIR, "weapons")

# Звук
DEFAULT_MUSIC_VOLUME = 0.5
DEFAULT_SFX_VOLUME = 0.7

# Оружие
WEAPON_DAMAGE = {
    "Pistol": 1,
    "Rifle": 3,
    "AssaultRifle": 1,
    "PlasmaRifle": 4,
    "GrenadeLauncher": 5
}
BURST_SHOTS = {
    "AssaultRifle": 3  # очередь из 3 выстрелов
}

# Настройки базы данных
DB_PATH = "saves/game_save.db"
