"""
Paddle module - player-controlled paddle
Author: Player1 (Game Logic)
"""

import pygame


class Paddle:
    """Player-controlled paddle."""

    def __init__(self, settings):
        self.settings = settings
        self.width = settings.PADDLE_WIDTH
        self.height = settings.PADDLE_HEIGHT
        self.color = settings.PADDLE_COLOR
        self.speed = settings.paddle_speed
        self.reset()

    def reset(self):
        self.x = (self.settings.SCREEN_WIDTH - self.width) / 2
        self.y = self.settings.SCREEN_HEIGHT - self.settings.PADDLE_Y_OFFSET - self.height

    def move_left(self):
        self.x = max(0, self.x - self.speed)

    def move_right(self):
        self.x = min(self.settings.SCREEN_WIDTH - self.width, self.x + self.speed)

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        rect = self.get_rect()
        # Paddle body with gradient-like effect
        pygame.draw.rect(surface, self.color, rect, border_radius=7)
        # Top highlight
        highlight = pygame.Rect(rect.x + 4, rect.y + 2, rect.width - 8, 4)
        pygame.draw.rect(surface, (200, 240, 255), highlight, border_radius=3)
        # Border
        pygame.draw.rect(surface, (180, 230, 255), rect, 2, border_radius=7)
