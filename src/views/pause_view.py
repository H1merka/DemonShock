import pygame
from typing import Callable, List
from src.views.ui_elements import Button, Slider
from src.controllers.audio_controller import AudioManager
from src.models.settings import FONT_PATH


class PauseMenu:
    """
    Pause menu UI with buttons and volume slider.

    Attributes:
        screen (pygame.Surface): Surface to draw the menu on.
        bg (pygame.Surface): Semi-transparent background overlay.
        on_resume (Callable): Callback to resume the game.
        on_save (Callable): Callback to save the game.
        on_quit_to_menu (Callable): Callback to quit to main menu.
        buttons (List[Button]): List of buttons in the pause menu.
        volume_slider (Slider): Slider controlling music volume.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        on_resume: Callable,
        on_save: Callable,
        on_quit_to_menu: Callable,
    ) -> None:
        self.screen = screen
        self.bg = pygame.Surface(screen.get_size())
        self.bg.set_alpha(180)
        self.bg.fill((0, 0, 0))

        self.on_resume = on_resume
        self.on_save = on_save
        self.on_quit_to_menu = on_quit_to_menu

        center_x = screen.get_width() // 2
        start_y = 250
        gap = 70

        self.buttons: List[Button] = [
            Button("Continue", (center_x, start_y), self.on_resume),
            Button("Save Game", (center_x, start_y + gap), self.on_save),
            Button("Quit to Menu", (center_x, start_y + 2 * gap), self.on_quit_to_menu),
        ]

        self.volume_slider = Slider(
            (center_x - 100, start_y + 3 * gap + 20),
            200,
            AudioManager.get_music_volume(),
        )

    def draw(self) -> None:
        """
        Draw the pause menu on the screen.
        """
        self.screen.blit(self.bg, (0, 0))
        font = pygame.font.Font(FONT_PATH, 36)
        title = font.render("Pause", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(self.screen)

        self.volume_slider.draw(self.screen)
        self.draw_volume_label()

    def draw_volume_label(self) -> None:
        """
        Draw the label for the volume slider.
        """
        font = pygame.font.Font(FONT_PATH, 24)
        text = font.render("Music Volume", True, (255, 255, 255))
        self.screen.blit(text, (self.volume_slider.x, self.volume_slider.y - 30))

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Handle events for buttons and volume slider, and update music volume.

        Args:
            events (List[pygame.event.Event]): List of pygame events to process.
        """
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

            self.volume_slider.handle_event(event)
            AudioManager.set_music_volume(self.volume_slider.value)
