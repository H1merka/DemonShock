# views/pause_view.py

import pygame
from src.views.ui_elements import Button, Slider
from src.controllers.audio_controller import AudioManager
from src.models.settings import FONT_PATH


class PauseMenu:
    def __init__(self, screen, on_resume, on_save, on_quit_to_menu):
        self.screen = screen
        self.bg = pygame.Surface(screen.get_size())
        self.bg.set_alpha(180)  # полупрозрачный фон
        self.bg.fill((0, 0, 0))

        self.on_resume = on_resume
        self.on_save = on_save
        self.on_quit_to_menu = on_quit_to_menu

        center_x = screen.get_width() // 2
        start_y = 250
        gap = 70

        self.buttons = [
            Button("Продолжить", (center_x, start_y), self.on_resume),
            Button("Сохранить игру", (center_x, start_y + gap), self.on_save),
            Button("Выйти в меню", (center_x, start_y + 2 * gap), self.on_quit_to_menu),
        ]

        self.volume_slider = Slider((center_x - 100, start_y + 3 * gap + 20), 200, AudioManager.get_music_volume())

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        font = pygame.font.Font(FONT_PATH, 36)
        title = font.render("Пауза", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(self.screen)

        self.volume_slider.draw(self.screen)
        self.draw_volume_label()

    def draw_volume_label(self):
        font = pygame.font.Font(FONT_PATH, 24)
        text = font.render("Громкость музыки", True, (255, 255, 255))
        self.screen.blit(text, (self.volume_slider.x, self.volume_slider.y - 30))

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

            self.volume_slider.handle_event(event)
            AudioManager.set_music_volume(self.volume_slider.value)
