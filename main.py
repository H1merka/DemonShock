# main.py

import pygame
from src.models.settings import *
from src.controllers.input_handler import InputHandler
from src.controllers.audio_controller import AudioManager
from src.controllers.level_manager import LevelManager
from src.views.menu_view import draw_main_menu, handle_menu_events
from src.views.pause_view import draw_pause_menu, handle_pause_events
from src.views.game_view import draw_game
from src.models.player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Demonic Invasion Shooter")
    clock = pygame.time.Clock()

    # Инициализация аудио
    AudioManager.init()
    # Запускаем музыку главного меню
    AudioManager.play_music('assets/music/menu_theme.ogg')

    input_handler = InputHandler()
    level_manager = LevelManager()
    player = Player(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2)

    game_state = 'menu'  # menu, playing, paused
    running = True

    while running:
        clock.tick(FPS)
        input_handler.process_events()

        if input_handler.quit_requested:
            running = False

        if game_state == 'menu':
            handle_menu_events(input_handler)
            draw_main_menu(screen)
            # Логика запуска игры по нажатию
            if input_handler.is_shooting:  # например, начать по пробелу/клику
                game_state = 'playing'
                AudioManager.play_music('assets/music/level1_theme.ogg')
                level_manager.start_level()

        elif game_state == 'playing':
            if input_handler.pause_requested:
                game_state = 'paused'
                AudioManager.set_music_volume(0.3)  # приглушить музыку в паузе

            # Обновление игрока
            move_x, move_y = input_handler.get_movement_vector()
            player.update(move_x, move_y, input_handler.is_shooting)

            # Обновление уровня и волн
            level_manager.update()

            # Отрисовка игрового экрана
            draw_game(screen, player, level_manager)

        elif game_state == 'paused':
            handle_pause_events(input_handler)
            draw_pause_menu(screen)
            if not input_handler.pause_requested:
                # Вернуться в игру по ESC или кнопке в меню паузы
                game_state = 'playing'
                AudioManager.set_music_volume(0.7)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
