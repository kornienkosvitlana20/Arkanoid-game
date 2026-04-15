"""
BrickGrid module - generates and manages all bricks
Author: Player1 (Game Logic)
"""

from brick import Brick
from settings import Settings


class BrickGrid:
    """Creates and manages the grid of bricks."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.bricks = []
        self._generate()

    def _generate(self):
        """Generate brick grid with varying HP per row."""
        self.bricks = []
        s = self.settings
        colors = s.BRICK_COLORS

        for row in range(s.BRICK_ROWS):
            for col in range(s.BRICK_COLS):
                x = col * (s.BRICK_WIDTH + s.BRICK_PADDING) + s.BRICK_PADDING
                y = row * (s.BRICK_HEIGHT + s.BRICK_PADDING) + s.BRICK_TOP_OFFSET

                color = colors[row % len(colors)]

                # Top rows have more HP
                if row < 2:
                    hp = 3
                elif row < 4:
                    hp = 2
                else:
                    hp = 1

                brick = Brick(x, y, color, hp)
                brick.width = s.BRICK_WIDTH
                brick.height = s.BRICK_HEIGHT
                self.bricks.append(brick)

    def reset(self):
        self._generate()

    def alive_bricks(self):
        return [b for b in self.bricks if b.alive]

    def all_cleared(self):
        return len(self.alive_bricks()) == 0

    def draw(self, surface):
        for brick in self.bricks:
            brick.draw(surface)
