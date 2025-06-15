# controllers/input_handler.py

import pygame

class InputHandler:
    def __init__(self):
        # Состояние клавиш для движения
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        # Стреляет ли игрок
        self.is_shooting = False

        # Позиция мыши (для прицеливания)
        self.mouse_pos = (0, 0)

        # Флаги для управления меню, паузой и прочим
        self.pause_requested = False
        self.quit_requested = False

    def process_events(self):
        self.pause_requested = False  # сброс перед новым циклом
        self.quit_requested = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_requested = True
                if event.key == pygame.K_w:
                    self.move_up = True
                if event.key == pygame.K_s:
                    self.move_down = True
                if event.key == pygame.K_a:
                    self.move_left = True
                if event.key == pygame.K_d:
                    self.move_right = True
                if event.key == pygame.K_SPACE:
                    self.is_shooting = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.move_up = False
                if event.key == pygame.K_s:
                    self.move_down = False
                if event.key == pygame.K_a:
                    self.move_left = False
                if event.key == pygame.K_d:
                    self.move_right = False
                if event.key == pygame.K_SPACE:
                    self.is_shooting = False

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши - тоже стрельба
                    self.is_shooting = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_shooting = False

    def get_movement_vector(self):
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
