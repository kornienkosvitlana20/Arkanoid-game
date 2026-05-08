"""
Tests for Paddle class (paddle.py)
Author: Player 2 — Вялкова Поліна
"""
import pytest
import pygame

pygame.init()

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from paddle import Paddle
from settings import Settings


pytestmark = pytest.mark.paddle


# ── Фікстури ──────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings(difficulty="medium")


@pytest.fixture
def paddle(settings):
    return Paddle(settings)


@pytest.fixture
def surface():
    return pygame.Surface((800, 600))


# ── Тести ініціалізації ───────────────────────────────────────────────────

class TestPaddleInit:
    """Перевірка початкового стану платформи."""

    def test_paddle_starts_centered(self, paddle, settings):
        """Платформа має починатися по центру екрану."""
        expected_x = (settings.SCREEN_WIDTH - settings.PADDLE_WIDTH) / 2
        assert paddle.x == expected_x

    def test_paddle_width_from_settings(self, paddle, settings):
        """Ширина платформи береться з налаштувань."""
        assert paddle.width == settings.PADDLE_WIDTH

    def test_paddle_height_from_settings(self, paddle, settings):
        """Висота платформи береться з налаштувань."""
        assert paddle.height == settings.PADDLE_HEIGHT

    def test_paddle_y_position(self, paddle, settings):
        """Платформа знаходиться на правильній висоті."""
        expected_y = settings.SCREEN_HEIGHT - settings.PADDLE_Y_OFFSET - settings.PADDLE_HEIGHT
        assert paddle.y == expected_y

    def test_paddle_speed_from_settings(self, paddle, settings):
        """Швидкість платформи береться з налаштувань."""
        assert paddle.speed == settings.paddle_speed


# ── Тести руху ────────────────────────────────────────────────────────────

class TestPaddleMovement:
    """Перевірка руху платформи."""

    def test_move_left_decreases_x(self, paddle):
        """move_left() зменшує координату x."""
        x_before = paddle.x
        paddle.move_left()
        assert paddle.x < x_before

    def test_move_right_increases_x(self, paddle):
        """move_right() збільшує координату x."""
        x_before = paddle.x
        paddle.move_right()
        assert paddle.x > x_before

    def test_move_left_by_speed(self, paddle):
        """move_left() переміщує платформу рівно на speed пікселів."""
        x_before = paddle.x
        paddle.move_left()
        assert paddle.x == x_before - paddle.speed

    def test_move_right_by_speed(self, paddle):
        """move_right() переміщує платформу рівно на speed пікселів."""
        x_before = paddle.x
        paddle.move_right()
        assert paddle.x == x_before + paddle.speed

    @pytest.mark.parametrize("steps", [1, 5, 10])
    def test_multiple_moves_right(self, paddle, steps):
        """Кілька кроків вправо переміщують платформу відповідно."""
        x_start = paddle.x
        for _ in range(steps):
            paddle.move_right()
        assert paddle.x == pytest.approx(x_start + paddle.speed * steps)


# ── Тести меж екрану ──────────────────────────────────────────────────────

class TestPaddleBoundaries:
    """Перевірка меж руху платформи."""

    def test_cannot_move_left_beyond_screen(self, paddle):
        """Платформа не виходить за ліву межу екрану."""
        paddle.x = 0
        paddle.move_left()
        assert paddle.x >= 0

    def test_cannot_move_right_beyond_screen(self, paddle, settings):
        """Платформа не виходить за праву межу екрану."""
        paddle.x = settings.SCREEN_WIDTH
        paddle.move_right()
        assert paddle.x + paddle.width <= settings.SCREEN_WIDTH

    def test_left_boundary_is_zero(self, paddle):
        """Ліва межа — x >= 0."""
        paddle.x = -100
        paddle.move_left()
        assert paddle.x >= 0

    def test_stays_at_left_wall(self, paddle):
        """При x=0 move_left() не змінює позицію."""
        paddle.x = 0
        paddle.move_left()
        assert paddle.x == 0


# ── Тести reset ───────────────────────────────────────────────────────────

class TestPaddleReset:
    """Перевірка методу reset."""

    def test_reset_centers_paddle(self, paddle, settings):
        """reset() повертає платформу до центру."""
        paddle.x = 0
        paddle.reset()
        expected_x = (settings.SCREEN_WIDTH - settings.PADDLE_WIDTH) / 2
        assert paddle.x == expected_x

    def test_reset_restores_y(self, paddle, settings):
        """reset() відновлює вертикальну позицію."""
        paddle.reset()
        expected_y = settings.SCREEN_HEIGHT - settings.PADDLE_Y_OFFSET - settings.PADDLE_HEIGHT
        assert paddle.y == expected_y


# ── Тести get_rect ────────────────────────────────────────────────────────

class TestPaddleRect:
    """Перевірка методу get_rect."""

    def test_rect_is_pygame_rect(self, paddle):
        """get_rect() повертає pygame.Rect."""
        assert isinstance(paddle.get_rect(), pygame.Rect)

    def test_rect_position_matches_paddle(self, paddle):
        """Rect відповідає позиції платформи."""
        rect = paddle.get_rect()
        assert rect.x == int(paddle.x)
        assert rect.y == int(paddle.y)

    def test_rect_size_matches_paddle(self, paddle):
        """Rect відповідає розмірам платформи."""
        rect = paddle.get_rect()
        assert rect.width == paddle.width
        assert rect.height == paddle.height


# ── Тести малювання ───────────────────────────────────────────────────────

class TestPaddleDraw:
    """Перевірка методу draw."""

    def test_draw_does_not_raise(self, paddle, surface):
        """draw() не кидає виключень."""
        try:
            paddle.draw(surface)
        except Exception as e:
            pytest.fail(f"draw() кинув виключення: {e}")
