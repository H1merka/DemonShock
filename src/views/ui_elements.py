# views/ui_elements.py

import pygame


class Button:
    def __init__(self, text, center_pos, callback, width=200, height=50, font_size=28):
        self.callback = callback
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center_pos

        self.base_color = (100, 0, 0)
        self.hover_color = (180, 0, 0)
        self.text_color = (255, 255, 255)

        self.font = pygame.font.Font("assets/fonts/rus_font.ttf", font_size)
        self.text = self.font.render(text, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        screen.blit(self.text, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class Slider:
    def __init__(self, pos, width, initial_value=0.5):
        self.x, self.y = pos
        self.width = width
        self.height = 10
        self.track_rect = pygame.Rect(self.x, self.y, width, self.height)
        self.handle_radius = 10

        self.value = max(0.0, min(1.0, initial_value))
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (60, 60, 60), self.track_rect)
        handle_x = self.x + int(self.value * self.width)
        pygame.draw.circle(screen, (200, 0, 0), (handle_x, self.y + self.height // 2), self.handle_radius)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._handle_rect().collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.value = (rel_x - self.x) / self.width

    def _handle_rect(self):
        handle_x = self.x + int(self.value * self.width)
        return pygame.Rect(handle_x - self.handle_radius, self.y, self.handle_radius * 2, self.height)
