# views/menu_view.py

import pygame
from src.views.ui_elements import Button, Slider
from src.controllers.audio_controller import AudioManager
from src.models.settings import UI_DIR, FONT_PATH


class MainMenu:
    def __init__(self, screen, on_new_game, on_continue_game, on_quit):
        self.screen = screen
        self.bg = pygame.image.load(UI_DIR + "main_menu_bg.png").convert()

        self.on_new_game = on_new_game
        self.on_continue_game = on_continue_game
        self.on_quit = on_quit

        self.buttons = [
            Button("Новая игра", (screen.get_width() // 2, 250), self.on_new_game),
            Button("Продолжить", (screen.get_width() // 2, 320), self.on_continue_game),
            Button("Выход", (screen.get_width() // 2, 390), self.on_quit)
        ]

        self.volume_slider = Slider((screen.get_width() // 2 - 100, 460), 200, AudioManager.get_music_volume())

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        for button in self.buttons:
            button.draw(self.screen)

        self.volume_slider.draw(self.screen)
        self.draw_volume_label()

    def draw_volume_label(self):
        font = pygame.font.Font(FONT_PATH, 24)
        text = font.render("Громкость музыки", True, (255, 255, 255))
        self.screen.blit(text, (self.volume_slider.rect.x, self.volume_slider.rect.y - 30))

    def handle_events(self, event_list):
        for event in event_list:
            for button in self.buttons:
                button.handle_event(event)

            self.volume_slider.handle_event(event)
            AudioManager.set_music_volume(self.volume_slider.value)
