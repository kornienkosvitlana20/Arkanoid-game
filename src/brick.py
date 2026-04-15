"""
Brick module - brick logic and rendering
Author: Player1 (Game Logic) + Player2 (Rendering)
"""

import pygame

# Brick: single brick with HP system
class Brick:
    """Single brick with HP, color, and score value."""

    # hp -> score multiplier
    SCORE_TABLE = {1: 10, 2: 20, 3: 30}

    def __init__(self, x, y, color, hp=1):
        self.x = x
        self.y = y
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.alive = True
        self.width = None   # set by BrickGrid
        self.height = None

    def hit(self):
        """Damage brick, return score if destroyed."""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return self.SCORE_TABLE.get(self.max_hp, 10)
        return 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface):
        if not self.alive:
            return
        rect = self.get_rect()

        # Darken color based on remaining hp
        factor = self.hp / self.max_hp
        color = tuple(int(c * (0.5 + 0.5 * factor)) for c in self.color)

        pygame.draw.rect(surface, color, rect, border_radius=4)

        # Crack effect for damaged bricks
        if self.hp < self.max_hp:
            crack_color = (255, 255, 255, 80)
            cx, cy = rect.centerx, rect.centery
            pygame.draw.line(surface, (50, 50, 50), (cx - 5, cy - 5), (cx + 3, cy + 3), 2)
            pygame.draw.line(surface, (50, 50, 50), (cx, cy - 6), (cx - 4, cy + 4), 2)

        # Top highlight
        pygame.draw.rect(surface, tuple(min(255, c + 60) for c in color),
                         pygame.Rect(rect.x + 3, rect.y + 2, rect.width - 6, 4),
                         border_radius=2)
        # Border
        pygame.draw.rect(surface, tuple(min(255, c + 40) for c in color),
                         rect, 2, border_radius=4)
