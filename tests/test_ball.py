"""
Tests for the Ball class.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
pygame.init()
pygame.display.set_mode((800, 600))

from ball import Ball
from settings import Settings


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings(difficulty="medium")


@pytest.fixture
def ball(settings):
    return Ball(settings)


# ── Settings tests ───────────────────────────────────────────────────────────

@pytest.mark.settings
class TestSettings:
    """Tests for the Settings class."""

    @pytest.mark.parametrize("difficulty,expected_speed", [
        ("easy", 5),
        ("medium", 7),
        ("hard", 9),
    ])
    def test_difficulty_ball_speed(self, difficulty, expected_speed):
        s = Settings(difficulty=difficulty)
        assert s.ball_speed == expected_speed

    @pytest.mark.parametrize("difficulty,expected_paddle_speed", [
        ("easy", 7),
        ("medium", 8),
        ("hard", 9),
    ])
    def test_difficulty_paddle_speed(self, difficulty, expected_paddle_speed):
        s = Settings(difficulty=difficulty)
        assert s.paddle_speed == expected_paddle_speed

    def test_default_lives(self):
        s = Settings()
        assert s.lives == 3

    def test_custom_lives(self):
        s = Settings(lives=5)
        assert s.lives == 5

    def test_bg_color_default(self):
        s = Settings()
        assert s.bg_color == (10, 10, 40)

    def test_bg_color_black(self):
        s = Settings(bg_color="black")
        assert s.bg_color == (0, 0, 0)

    def test_bg_color_unknown_fallback(self):
        s = Settings(bg_color="nonexistent")
        assert s.bg_color == (10, 10, 40)

    def test_screen_dimensions(self):
        s = Settings()
        assert s.SCREEN_WIDTH == 800
        assert s.SCREEN_HEIGHT == 600

    def test_brick_grid_dimensions(self):
        s = Settings()
        assert s.BRICK_ROWS == 6
        assert s.BRICK_COLS == 10


# ── Ball tests ───────────────────────────────────────────────────────────────

@pytest.mark.ball
class TestBallInit:
    """Tests for Ball initialization and reset."""

    def test_ball_starts_inactive(self, ball):
        assert ball.active is False

    def test_ball_radius(self, ball, settings):
        assert ball.radius == settings.BALL_RADIUS

    def test_ball_initial_position_centered(self, ball, settings):
        assert ball.x == settings.SCREEN_WIDTH / 2

    def test_ball_reset_position(self, ball, settings):
        ball.x = 100
        ball.y = 100
        ball.reset()
        assert ball.x == settings.SCREEN_WIDTH / 2

    def test_ball_launch_sets_active(self, ball):
        ball.launch()
        assert ball.active is True


@pytest.mark.ball
class TestBallMovement:
    """Tests for Ball movement and wall bouncing."""

    def test_ball_does_not_move_when_inactive(self, ball):
        ball.active = False
        x_before = ball.x
        y_before = ball.y
        ball.update()
        assert ball.x == x_before
        assert ball.y == y_before

    def test_ball_moves_when_active(self, ball):
        ball.launch()
        ball.vx = 5
        ball.vy = -5
        x_before = ball.x
        ball.update()
        assert ball.x != x_before

    def test_bounce_off_left_wall(self, ball):
        ball.launch()
        ball.x = ball.radius - 1
        ball.vx = -5
        ball._bounce_walls()
        assert ball.vx > 0

    def test_bounce_off_right_wall(self, ball, settings):
        ball.launch()
        ball.x = settings.SCREEN_WIDTH - ball.radius + 1
        ball.vx = 5
        ball._bounce_walls()
        assert ball.vx < 0

    def test_bounce_off_top_wall(self, ball):
        ball.launch()
        ball.y = ball.radius - 1
        ball.vy = -5
        ball._bounce_walls()
        assert ball.vy > 0

    def test_is_lost_below_screen(self, ball, settings):
        ball.y = settings.SCREEN_HEIGHT + ball.radius + 1
        assert ball.is_lost() is True

    def test_not_lost_on_screen(self, ball):
        ball.y = 300
        assert ball.is_lost() is False


@pytest.mark.ball
class TestBallPaddleCollision:
    """Tests for Ball-Paddle collision."""

    def test_no_collision_when_inactive(self, ball, settings):
        from paddle import Paddle
        paddle = Paddle(settings)
        ball.active = False
        ball.vy = 5
        ball.x = paddle.x + paddle.width / 2
        ball.y = paddle.y - ball.radius - 1
        ball.check_paddle_collision(paddle)
        # vy should remain unchanged since ball is inactive
        assert ball.vy == 5

    def test_collision_reverses_vy(self, ball, settings):
        from paddle import Paddle
        paddle = Paddle(settings)
        ball.launch()
        ball.vy = 5   # moving downward
        ball.x = paddle.x + paddle.width / 2
        ball.y = paddle.y + paddle.height / 2
        ball.check_paddle_collision(paddle)
        assert ball.vy < 0  # must bounce up

    def test_no_collision_when_moving_up(self, ball, settings):
        from paddle import Paddle
        paddle = Paddle(settings)
        ball.launch()
        ball.vy = -5  # already moving up
        ball.x = paddle.x + paddle.width / 2
        ball.y = paddle.y + paddle.height / 2
        ball.check_paddle_collision(paddle)
        assert ball.vy == -5  # unchanged


@pytest.mark.ball
class TestBallBrickCollision:
    """Tests for Ball-Brick collision."""

    def test_collision_with_alive_brick_returns_score(self, ball, settings):
        from brick import Brick
        brick = Brick(100, 100, (255, 0, 0), hp=1)
        brick.width = settings.BRICK_WIDTH
        brick.height = settings.BRICK_HEIGHT

        ball.launch()
        ball.x = brick.x + brick.width / 2
        ball.y = brick.y + brick.height / 2

        score = ball.check_brick_collision([brick])
        assert score == 10
        assert brick.alive is False

    def test_no_collision_with_dead_brick(self, ball, settings):
        from brick import Brick
        brick = Brick(100, 100, (255, 0, 0), hp=1)
        brick.width = settings.BRICK_WIDTH
        brick.height = settings.BRICK_HEIGHT
        brick.alive = False

        ball.launch()
        ball.x = brick.x + brick.width / 2
        ball.y = brick.y + brick.height / 2

        score = ball.check_brick_collision([brick])
        assert score == 0

    def test_no_collision_when_far_from_brick(self, ball, settings):
        from brick import Brick
        brick = Brick(600, 400, (255, 0, 0), hp=1)
        brick.width = settings.BRICK_WIDTH
        brick.height = settings.BRICK_HEIGHT

        ball.launch()
        ball.x = 10
        ball.y = 10

        score = ball.check_brick_collision([brick])
        assert score == 0
        assert brick.alive is True
