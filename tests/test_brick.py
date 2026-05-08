"""
Tests for Brick class (brick.py)
Author: Player 1 — Корнієнко Світлана
"""
import pytest
import pygame

pygame.init()

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from brick import Brick


pytestmark = pytest.mark.brick


# ── Фікстури ──────────────────────────────────────────────────────────────

@pytest.fixture
def simple_brick():
    """Звичайна цеглина hp=1."""
    b = Brick(50, 100, (255, 80, 80), hp=1)
    b.width = 70
    b.height = 22
    return b


@pytest.fixture
def strong_brick():
    """Міцна цеглина hp=3."""
    b = Brick(50, 100, (255, 80, 80), hp=3)
    b.width = 70
    b.height = 22
    return b


@pytest.fixture
def surface():
    return pygame.Surface((800, 600))


# ── Тести ініціалізації ───────────────────────────────────────────────────

class TestBrickInit:
    """Перевірка початкового стану цеглини."""

    def test_brick_starts_alive(self, simple_brick):
        """Цеглина при створенні має бути живою."""
        assert simple_brick.alive is True

    def test_brick_stores_hp(self, strong_brick):
        """HP має зберігатись правильно."""
        assert strong_brick.hp == 3

    def test_brick_stores_max_hp(self, strong_brick):
        """max_hp має дорівнювати початковому hp."""
        assert strong_brick.max_hp == 3

    def test_brick_position(self, simple_brick):
        """Позиція цеглини має зберігатись."""
        assert simple_brick.x == 50
        assert simple_brick.y == 100

    def test_brick_color(self):
        """Колір цеглини має зберігатись."""
        color = (100, 200, 50)
        b = Brick(0, 0, color, hp=1)
        assert b.color == color


# ── Тести системи HP ──────────────────────────────────────────────────────

class TestBrickHit:
    """Перевірка системи HP та методу hit()."""

    def test_single_hit_destroys_hp1_brick(self, simple_brick):
        """Один удар знищує цеглину з hp=1."""
        simple_brick.hit()
        assert simple_brick.alive is False

    def test_hit_reduces_hp(self, strong_brick):
        """Удар зменшує HP на 1."""
        hp_before = strong_brick.hp
        strong_brick.hit()
        assert strong_brick.hp == hp_before - 1

    def test_hp3_brick_survives_two_hits(self, strong_brick):
        """Цеглина hp=3 виживає після 2 ударів."""
        strong_brick.hit()
        strong_brick.hit()
        assert strong_brick.alive is True

    def test_hp3_brick_destroyed_after_three_hits(self, strong_brick):
        """Цеглина hp=3 знищується після 3 ударів."""
        strong_brick.hit()
        strong_brick.hit()
        strong_brick.hit()
        assert strong_brick.alive is False

    @pytest.mark.parametrize("hp,expected_score", [
        (1, 10),
        (2, 20),
        (3, 30),
    ])
    def test_score_returned_on_destroy(self, hp, expected_score):
        """Перевірка таблиці очок при знищенні цеглини."""
        b = Brick(0, 0, (255, 0, 0), hp=hp)
        b.width = 70
        b.height = 22
        total_score = 0
        for _ in range(hp):
            total_score = b.hit()
        assert total_score == expected_score

    def test_hit_returns_zero_before_destroy(self, strong_brick):
        """hit() повертає 0, поки цеглина не знищена."""
        score = strong_brick.hit()
        assert score == 0

    def test_hit_returns_score_on_destroy(self, simple_brick):
        """hit() повертає ненульові очки при знищенні."""
        score = simple_brick.hit()
        assert score > 0


# ── Тести get_rect ────────────────────────────────────────────────────────

class TestBrickRect:
    """Перевірка методу get_rect."""

    def test_rect_position(self, simple_brick):
        """Rect має правильну позицію."""
        rect = simple_brick.get_rect()
        assert rect.x == 50
        assert rect.y == 100

    def test_rect_size(self, simple_brick):
        """Rect має правильні розміри."""
        rect = simple_brick.get_rect()
        assert rect.width == 70
        assert rect.height == 22

    def test_rect_is_pygame_rect(self, simple_brick):
        """get_rect() повертає pygame.Rect."""
        assert isinstance(simple_brick.get_rect(), pygame.Rect)


# ── Тести малювання ───────────────────────────────────────────────────────

class TestBrickDraw:
    """Перевірка методу draw."""

    def test_alive_brick_draws_without_error(self, simple_brick, surface):
        """Жива цеглина малюється без помилок."""
        try:
            simple_brick.draw(surface)
        except Exception as e:
            pytest.fail(f"draw() кинув виключення: {e}")

    def test_dead_brick_does_not_draw(self, simple_brick, surface):
        """Мертва цеглина не повинна малюватись (метод одразу виходить)."""
        simple_brick.alive = False
        # Просто перевіряємо що не кидає помилку
        try:
            simple_brick.draw(surface)
        except Exception as e:
            pytest.fail(f"draw() для мертвої цеглини кинув виключення: {e}")

    def test_damaged_brick_draws_crack(self, strong_brick, surface):
        """Пошкоджена цеглина малюється без помилок (crack effect)."""
        strong_brick.hit()  # hp знижено, активується crack
        try:
            strong_brick.draw(surface)
        except Exception as e:
            pytest.fail(f"draw() пошкодженої цеглини кинув виключення: {e}")
