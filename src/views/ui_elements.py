import pygame
from typing import Callable, Tuple
from src.models.settings import FONT_PATH


class Button:
    """
    A clickable button UI element.

    Attributes:
        callback (Callable): Function to call when the button is clicked.
        rect (pygame.Rect): Rectangle defining button position and size.
        base_color (Tuple[int, int, int]): Default button color.
        hover_color (Tuple[int, int, int]): Button color when hovered by mouse.
        text_color (Tuple[int, int, int]): Text color.
        border_color (Tuple[int, int, int]): Border color.
        border_width (int): Border thickness.
        font (pygame.font.Font): Font used for button text.
        text (pygame.Surface): Rendered text surface.
        text_rect (pygame.Rect): Rectangle for centering the text.
    """

    def __init__(self, text: str, center_pos: Tuple[int, int], callback: Callable, width: int = 200, height: int = 50, font_size: int = 50) -> None:
        self.callback = callback
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center_pos

        self.base_color = (100, 0, 0)
        self.hover_color = (180, 0, 0)
        self.text_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.border_width = 3

        self.font = pygame.font.Font(FONT_PATH, font_size)
        self.text = self.font.render(text, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button on the screen.

        Args:
            screen (pygame.Surface): Surface to draw the button on.
        """
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width, border_radius=12)
        screen.blit(self.text, self.text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle mouse events and trigger callback on click.

        Args:
            event (pygame.event.Event): The pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class Slider:
    """
    A horizontal slider UI element for selecting a value between 0 and 1.

    Attributes:
        x (int): X-coordinate of the slider track start.
        y (int): Y-coordinate of the slider track.
        width (int): Width of the slider track.
        height (int): Height of the slider track.
        track_rect (pygame.Rect): Rectangle representing the slider track.
        handle_radius (int): Radius of the draggable handle circle.
        value (float): Current slider value (0.0 to 1.0).
        dragging (bool): Whether the handle is currently being dragged.
        rect (pygame.Rect): Rectangle covering the slider (for event handling).
    """

    def __init__(self, pos: Tuple[int, int], width: int, initial_value: float = 0.5) -> None:
        self.x, self.y = pos
        self.width = width
        self.height = 10
        self.track_rect = pygame.Rect(self.x, self.y, width, self.height)
        self.handle_radius = 10

        self.value = max(0.0, min(1.0, initial_value))
        self.dragging = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the slider track and handle.

        Args:
            screen (pygame.Surface): Surface to draw the slider on.
        """
        pygame.draw.rect(screen, (60, 60, 60), self.track_rect)
        handle_x = self.x + int(self.value * self.width)
        pygame.draw.circle(screen, (200, 0, 0), (handle_x, self.y + self.height // 2), self.handle_radius)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle mouse events to update the slider value.

        Args:
            event (pygame.event.Event): The pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._handle_rect().collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.value = (rel_x - self.x) / self.width

    def _handle_rect(self) -> pygame.Rect:
        """
        Get the rectangle area of the slider handle.

        Returns:
            pygame.Rect: Rectangle covering the handle area.
        """
        handle_x = self.x + int(self.value * self.width)
        return pygame.Rect(handle_x - self.handle_radius, self.y, self.handle_radius * 2, self.height)
