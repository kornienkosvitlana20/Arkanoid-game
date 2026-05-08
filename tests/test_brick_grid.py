"""
Tests for BrickGrid class (brick_grid.py)
Author: Player 1 — Корнієнко Світлана
"""
import pytest
import pygame

pygame.init()

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from brick_grid import BrickGrid
from settings import Settings


pytestmark = pytest.mark.brick_grid


# ── Фікстури ──────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings(difficulty="medium")


@pytest.fixture
def grid(settings):
    return BrickGrid(settings)


@pytest.fixture
def surface():
    return pygame.Surface((800, 600))


# ── Тести генерації ───────────────────────────────────────────────────────

class TestBrickGridGeneration:
    """Перевірка генерації сітки цеглин."""

    def test_total_brick_count(self, grid, settings):
        """Кількість цеглин = BRICK_ROWS × BRICK_COLS."""
        expected = settings.BRICK_ROWS * settings.BRICK_COLS
        assert len(grid.bricks) == expected

    def test_all_bricks_start_alive(self, grid):
        """Всі цеглини при генерації живі."""
        assert all(b.alive for b in grid.bricks)

    def test_top_rows_have_hp3(self, grid, settings):
        """Перші 2 ряди мають hp=3."""
        top_bricks = [b for b in grid.bricks
                      if b.y < settings.BRICK_TOP_OFFSET +
                      2 * (settings.BRICK_HEIGHT + settings.BRICK_PADDING)]
        assert all(b.hp == 3 for b in top_bricks)

    def test_bottom_rows_have_hp1(self, grid, settings):
        """Останні ряди (4+) мають hp=1."""
        threshold_y = (settings.BRICK_TOP_OFFSET +
                       4 * (settings.BRICK_HEIGHT + settings.BRICK_PADDING))
        bottom_bricks = [b for b in grid.bricks if b.y >= threshold_y]
        assert all(b.hp == 1 for b in bottom_bricks)

    def test_bricks_have_correct_size(self, grid, settings):
        """Всі цеглини мають правильні розміри."""
        for b in grid.bricks:
            assert b.width == settings.BRICK_WIDTH
            assert b.height == settings.BRICK_HEIGHT

    def test_bricks_have_valid_positions(self, grid, settings):
        """Всі цеглини знаходяться в межах екрану по горизонталі."""
        for b in grid.bricks:
            assert b.x >= 0
            assert b.x + b.width <= settings.SCREEN_WIDTH + settings.BRICK_PADDING


# ── Тести alive_bricks / all_cleared ─────────────────────────────────────

class TestBrickGridState:
    """Перевірка стану сітки."""

    def test_alive_bricks_returns_all_initially(self, grid, settings):
        """Спочатку alive_bricks() повертає всі цеглини."""
        expected = settings.BRICK_ROWS * settings.BRICK_COLS
        assert len(grid.alive_bricks()) == expected

    def test_all_cleared_false_initially(self, grid):
        """all_cleared() = False якщо є живі цеглини."""
        assert grid.all_cleared() is False

    def test_all_cleared_true_when_all_dead(self, grid):
        """all_cleared() = True коли всі цеглини знищені."""
        for brick in grid.bricks:
            brick.alive = False
        assert grid.all_cleared() is True

    def test_alive_bricks_decreases_after_kill(self, grid):
        """alive_bricks() зменшується після знищення цеглини."""
        count_before = len(grid.alive_bricks())
        grid.bricks[0].alive = False
        count_after = len(grid.alive_bricks())
        assert count_after == count_before - 1

    def test_partial_clear(self, grid):
        """Якщо жива хоча б одна цеглина — all_cleared() = False."""
        for brick in grid.bricks[:-1]:
            brick.alive = False
        assert grid.all_cleared() is False


# ── Тести reset ───────────────────────────────────────────────────────────

class TestBrickGridReset:
    """Перевірка методу reset."""

    def test_reset_restores_all_bricks(self, grid, settings):
        """Після reset кількість цеглин знову повна."""
        for brick in grid.bricks:
            brick.alive = False

        grid.reset()

        expected = settings.BRICK_ROWS * settings.BRICK_COLS
        assert len(grid.bricks) == expected

    def test_reset_makes_all_bricks_alive(self, grid):
        """Після reset всі цеглини живі."""
        for brick in grid.bricks:
            brick.alive = False

        grid.reset()

        assert all(b.alive for b in grid.bricks)

    def test_reset_does_not_clear_false(self, grid):
        """Після reset all_cleared() = False (є живі цеглини)."""
        grid.reset()
        assert grid.all_cleared() is False


# ── Тести малювання ───────────────────────────────────────────────────────

class TestBrickGridDraw:
    """Перевірка методу draw."""

    def test_draw_does_not_raise(self, grid, surface):
        """draw() не кидає виключень."""
        try:
            grid.draw(surface)
        except Exception as e:
            pytest.fail(f"draw() кинув виключення: {e}")

    def test_draw_with_dead_bricks_does_not_raise(self, grid, surface):
        """draw() з мертвими цеглинами не кидає виключень."""
        for brick in grid.bricks:
            brick.alive = False
        try:
            grid.draw(surface)
        except Exception as e:
            pytest.fail(f"draw() кинув виключення: {e}")
