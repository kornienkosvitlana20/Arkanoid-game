"""
Settings module - handles all game configuration
Author: Player2 (UI/Configuration)
"""

BG_COLORS = {
    "dark_blue":   (10, 10, 40),
    "black":       (0, 0, 0),
    "dark_purple": (20, 0, 40),
    "dark_green":  (0, 20, 10),
}
# difficulty levels: easy, medium, hard
DIFFICULTY_SETTINGS = {
    "easy": {
        "ball_speed": 5,
        "paddle_speed": 7,
        "ball_speed_increment": 0.3,
        "max_ball_speed": 10,
    },
    "medium": {
        "ball_speed": 7,
        "paddle_speed": 8,
        "ball_speed_increment": 0.5,
        "max_ball_speed": 14,
    },
    "hard": {
        "ball_speed": 9,
        "paddle_speed": 9,
        "ball_speed_increment": 0.7,
        "max_ball_speed": 18,
    },
}


class Settings:
    """Stores all game settings."""

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    TITLE = "Arkanoid"

    # Paddle
    PADDLE_WIDTH = 100
    PADDLE_HEIGHT = 14
    PADDLE_Y_OFFSET = 40

    # Ball
    BALL_RADIUS = 9

    # Bricks
    BRICK_ROWS = 6
    BRICK_COLS = 10
    BRICK_WIDTH = 70
    BRICK_HEIGHT = 22
    BRICK_PADDING = 5
    BRICK_TOP_OFFSET = 60

    # Colors
    PADDLE_COLOR = (100, 200, 255)
    BALL_COLOR = (255, 230, 100)
    TEXT_COLOR = (255, 255, 255)
    BORDER_COLOR = (60, 60, 120)

    BRICK_COLORS = [
        (255, 80,  80),
        (255, 150, 50),
        (255, 220, 50),
        (80,  220, 80),
        (50,  180, 255),
        (180, 80,  255),
    ]

    def __init__(self, difficulty="medium", bg_color="dark_blue", lives=3, fullscreen=False):
        self.difficulty = difficulty
        self.bg_color = BG_COLORS.get(bg_color, BG_COLORS["dark_blue"])
        self.lives = lives
        self.fullscreen = fullscreen

        diff = DIFFICULTY_SETTINGS[difficulty]
        self.ball_speed = diff["ball_speed"]
        self.paddle_speed = diff["paddle_speed"]
        self.ball_speed_increment = diff["ball_speed_increment"]
        self.max_ball_speed = diff["max_ball_speed"]
