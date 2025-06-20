import pygame
from typing import Callable, List
from src.views.ui_elements import Button, Slider
from src.controllers.audio_controller import AudioManager
from src.models.settings import UI_DIR, FONT_PATH


class MainMenu:
    """
    Main menu UI with background, buttons, and volume slider.

    Attributes:
        screen (pygame.Surface): Surface to draw the menu on.
        bg (pygame.Surface): Background image.
        on_new_game (Callable): Callback for starting a new game.
        on_continue_game (Callable): Callback for continuing a saved game.
        on_quit (Callable): Callback for quitting the game.
        buttons (List[Button]): List of menu buttons.
        volume_slider (Slider): Slider controlling music volume.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        on_new_game: Callable,
        on_continue_game: Callable,
        on_quit: Callable,
    ) -> None:
        self.screen = screen
        self.bg = pygame.image.load(UI_DIR + "/main_menu_bg.png").convert()

        self.on_new_game = on_new_game
        self.on_continue_game = on_continue_game
        self.on_quit = on_quit

        center_x = screen.get_width() // 2

        self.buttons: List[Button] = [
            Button("New Game", (center_x, 250), self.on_new_game),
            Button("Continue", (center_x, 320), self.on_continue_game),
            Button("Quit", (center_x, 390), self.on_quit),
        ]

        self.volume_slider = Slider((center_x - 100, 460), 200, AudioManager.get_music_volume())

    def draw(self) -> None:
        """
        Draw the main menu including background, buttons, and volume slider.
        """
        self.screen.blit(self.bg, (0, 0))

        self.draw_title()

        for button in self.buttons:
            button.draw(self.screen)

        self.volume_slider.draw(self.screen)
        self.draw_volume_label()

    def draw_title(self) -> None:
        """
        Draw the game title on the screen.
        """
        title_font = pygame.font.Font(FONT_PATH, 200)
        title_text = title_font.render("DemonShock", True, (200, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title_text, title_rect)

    def draw_volume_label(self) -> None:
        """
        Draw the label for the volume slider above it, centered horizontally.
        """
        font = pygame.font.Font(FONT_PATH, 38)
        text = font.render("Music Volume", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = self.volume_slider.x + self.volume_slider.width // 2
        text_rect.bottom = self.volume_slider.y - 5
        self.screen.blit(text, text_rect)

    def handle_events(self, event_list: List[pygame.event.Event]) -> None:
        """
        Handle events for buttons and volume slider and update music volume.

        Args:
            event_list (List[pygame.event.Event]): List of pygame events to process.
        """
        for event in event_list:
            for button in self.buttons:
                button.handle_event(event)

            self.volume_slider.handle_event(event)
            AudioManager.set_music_volume(self.volume_slider.value)
