import pygame
from src.models.settings import *
from src.controllers.input_handler import InputHandler
from src.controllers.audio_controller import AudioManager
from src.controllers.level_manager import LevelManager
from src.views.menu_view import MainMenu
from src.views.pause_view import PauseMenu
from src.views.game_view import GameView
from src.models.player import Player
from src.models.database import SaveManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DemonShock")
    clock = pygame.time.Clock()
    icon_surface = pygame.image.load(ICON_PATH).convert_alpha()
    pygame.display.set_icon(icon_surface)

    # Инициализация аудио
    AudioManager.init()
    # Запускаем музыку главного меню
    AudioManager.play_music(MUSIC_DIR+'/menu.ogg')

    # Загрузка звуков оружия
    AudioManager.load_weapon_sfx("Pistol", SFX_DIR+"/pistol.wav")
    AudioManager.load_weapon_sfx("Rifle", SFX_DIR+"/rifle.wav")
    AudioManager.load_weapon_sfx("AssaultRifle", SFX_DIR+"/pistol.wav")
    AudioManager.load_weapon_sfx("PlasmaRifle", SFX_DIR+"/plasma.wav")
    AudioManager.load_weapon_sfx("GrenadeLauncher", SFX_DIR+"/rlaunch.wav")

    # Загрузка звуков появления врагов
    AudioManager.load_enemy_spawn_sfx("jumper", SFX_DIR + "/jumper.wav")
    AudioManager.load_enemy_spawn_sfx("shooter", SFX_DIR + "/shooter.wav")
    AudioManager.load_enemy_spawn_sfx("warrior", SFX_DIR + "/warrior.wav")
    AudioManager.load_enemy_spawn_sfx("tank", SFX_DIR + "/tank.wav")
    AudioManager.load_enemy_spawn_sfx("summoner", SFX_DIR + "/summoner.wav")

    # Загрузка звуков появления боссов
    AudioManager.load_boss_spawn_sfx("ShooterBoss", SFX_DIR+"/boss_shooter.wav")
    AudioManager.load_boss_spawn_sfx("TankBoss", SFX_DIR+"/boss_tank.wav")
    AudioManager.load_boss_spawn_sfx("SummonerBoss", SFX_DIR+"/boss_summoner.wav")

    # ====== Загрузка звука шагов ======
    AudioManager.load_step_sfx(SFX_DIR + "/steps.wav")  # <- добавлено

    input_handler = InputHandler()
    level_manager = LevelManager()
    save_manager = SaveManager()
    player = Player(pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    game_view = None  # инициализируем позже, после старта уровня

    game_state = 'menu'  # menu, playing, paused
    running = True

    # Функции-заглушки для обработки кнопок меню
    def start_game():
        nonlocal game_state, game_view
        game_state = 'playing'
        AudioManager.play_music(MUSIC_DIR+'/abyss.ogg')
        level_manager.start_level()

        map_surface = level_manager.get_map_surface()
        player.set_collision_mask(level_manager.get_collision_mask())

        game_view = GameView(
            screen=screen,
            map=map_surface,
            player=player,
            enemies=level_manager.get_sprite_groups()["enemies"],
            projectiles=level_manager.get_projectile_group(),
            boss=level_manager.get_entities()["boss"]
        )

    def continue_game():
        # Добавь логику загрузки/продолжения, если нужно
        nonlocal game_state, game_view
        saved = save_manager.load_last_game()
        if saved:
            level_manager.start_level(saved['level'])
            player.health = saved['health']
            player.switch_weapon(saved['weapon'])
            AudioManager.set_music_volume(saved['music_volume'])
            AudioManager.play_music(MUSIC_DIR + '/abyss.ogg')

            map_surface = level_manager.get_map_surface()
            player.set_collision_mask(level_manager.get_collision_mask())

            game_view = GameView(
                screen=screen,
                map=map_surface,
                player=player,
                enemies=level_manager.get_sprite_groups()["enemies"],
                projectiles=level_manager.get_projectile_group(),
                boss=level_manager.get_entities()["boss"]
            )
            game_state = 'playing'

    def quit_game():
        nonlocal running
        running = False

    def resume_game():
        nonlocal game_state
        game_state = 'playing'
        AudioManager.set_music_volume(0.7)

    def save_game():
        current_weapon = player.weapon.name if player.weapon else "Pistol"
        save_manager.save_game(
            level=level_manager.current_level,
            health=player.health,
            weapon_name=current_weapon,
            music_volume=AudioManager.get_music_volume()
        )

    def quit_to_menu():
        nonlocal game_state
        game_state = 'menu'
        AudioManager.play_music(MUSIC_DIR + '/menu.ogg')

    # Объекты меню
    menu = MainMenu(screen, on_new_game=start_game, on_continue_game=continue_game, on_quit=quit_game)
    pause_menu = PauseMenu(screen, on_resume=resume_game, on_save=save_game, on_quit_to_menu=quit_to_menu)

    while running:
        event_list = pygame.event.get()

        input_handler.process_events(event_list)

        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        if game_state == 'menu':
            menu.handle_events(event_list)
            menu.draw()

        elif game_state == 'playing':
            if input_handler.pause_requested:
                game_state = 'paused'
                AudioManager.set_music_volume(0.3)

            dt = clock.tick(FPS) / 1000

            player.update(input_handler.get_movement_vector(), dt=dt)
            level_manager.update(dt)

            # === Стрельба по нажатию мыши ===
            if pygame.mouse.get_pressed()[0]:  # ЛКМ
                mouse_pos = pygame.mouse.get_pos()
                current_time = pygame.time.get_ticks()
                player.shoot(mouse_pos, current_time, level_manager.get_projectile_group())

            # === Обновление game_view ===
            if game_view:
                game_view.enemies = level_manager.get_sprite_groups()["enemies"]
                game_view.projectiles = level_manager.get_projectile_group()
                game_view.boss = level_manager.get_entities()["boss"]
                game_view.draw()

        elif game_state == 'paused':
            pause_menu.handle_events(event_list)
            pause_menu.draw()

        pygame.display.flip()

    save_manager.close()
    pygame.quit()


if __name__ == "__main__":
    main()
