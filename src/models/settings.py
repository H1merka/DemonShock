import os

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Player
PLAYER_SPEED = 5
PLAYER_HEALTH = 3

# Enemies and bosses
ENEMY_HEALTH = 2
BOSS_HEALTH = 100

# Levels
WAVES_PER_LEVEL = 5
ENEMY_SCALE_FACTOR = 1.5  # increase the number of enemies every 3 levels

# Ways to assets
ASSET_DIR = "assets"
FONT_PATH = os.path.join(ASSET_DIR, "fonts", "russian_font.ttf")
MAPS_DIR = os.path.join(ASSET_DIR, "maps")
SPRITE_DIR = os.path.join(ASSET_DIR, "sprites")
ICON_PATH = os.path.join(ASSET_DIR, "icons", "game_icon.png")
MUSIC_DIR = os.path.join(ASSET_DIR, "music")
SFX_DIR = os.path.join(ASSET_DIR, "sfx")
UI_DIR = os.path.join(ASSET_DIR, "ui")
WEAPON_SPRITES_DIR = os.path.join(ASSET_DIR, "weapons")
MAP_IMG = [
    MAPS_DIR+"/map1.jpg",
    MAPS_DIR+"/map2.jpg",
    MAPS_DIR+"/map3.jpg",
]

# Sound
DEFAULT_MUSIC_VOLUME = 0.5
DEFAULT_SFX_VOLUME = 0.7

# Weapons
WEAPON_DAMAGE = {
    "Pistol": 1,
    "Rifle": 3,
    "AssaultRifle": 1,
    "PlasmaRifle": 4,
    "GrenadeLauncher": 5
}

# Database
DB_PATH = "saves/game_save.db"
