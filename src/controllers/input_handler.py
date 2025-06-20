import pygame
from typing import List, Tuple


class InputHandler:
    """
    Handles keyboard and mouse input state for player movement,
    shooting, and game control such as pause and quit.
    """

    def __init__(self) -> None:
        # Movement key states
        self.move_up: bool = False
        self.move_down: bool = False
        self.move_left: bool = False
        self.move_right: bool = False

        # Shooting state
        self.is_shooting: bool = False

        # Mouse position for aiming
        self.mouse_pos: Tuple[int, int] = (0, 0)

        # Flags for menu control and quitting the game
        self.pause_requested: bool = False
        self.quit_requested: bool = False

    def process_events(self, events: List[pygame.event.Event]) -> None:
        """
        Process a list of pygame events to update input states.

        Args:
            events (List[pygame.event.Event]): List of events to process.
        """
        self.pause_requested = False  # reset before processing new events
        self.quit_requested = False

        for event in events:
            if event.type == pygame.QUIT:
                self.quit_requested = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_requested = True
                elif event.key == pygame.K_w:
                    self.move_up = True
                elif event.key == pygame.K_s:
                    self.move_down = True
                elif event.key == pygame.K_a:
                    self.move_left = True
                elif event.key == pygame.K_d:
                    self.move_right = True
                elif event.key == pygame.K_SPACE:
                    self.is_shooting = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.move_up = False
                elif event.key == pygame.K_s:
                    self.move_down = False
                elif event.key == pygame.K_a:
                    self.move_left = False
                elif event.key == pygame.K_d:
                    self.move_right = False
                elif event.key == pygame.K_SPACE:
                    self.is_shooting = False

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button for shooting
                    self.is_shooting = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_shooting = False

    def get_movement_vector(self) -> Tuple[int, int]:
        """
        Calculate the movement vector based on current input states.

        Returns:
            Tuple[int, int]: Movement vector (x, y), each component can be -1, 0, or 1.
        """
        x = 0
        y = 0
        if self.move_up:
            y -= 1
        if self.move_down:
            y += 1
        if self.move_left:
            x -= 1
        if self.move_right:
            x += 1
        return x, y
