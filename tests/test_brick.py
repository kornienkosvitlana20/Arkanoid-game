"""
Tests for the Brick and BrickGrid classes.
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

from brick import Brick
from brick_grid import BrickGrid
from settings import Settings


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def simple_brick():
    brick = Brick(x=100, y=50, color=(255, 0, 0), hp=1)
    brick.width = 70
    brick.height = 22
    return brick


@pytest.fixture
def strong_brick():
    brick = Brick(x=100, y=50, color=(255, 100, 0), hp=3)
    brick.width = 70
    brick.height = 22
    return brick


@pytest.fixture
def grid(settings):
    return BrickGrid(settings)


# ── Brick init tests ──────────────────────────────────────────────────────────

@pytest.mark.brick
class TestBrickInit:
    """Tests for Brick initialization."""

    def test_brick_starts_alive(self, simple_brick):
        assert simple_brick.alive is True

    def test_brick_hp(self, simple_brick):
        assert simple_brick.hp == 1

    def test_brick_max_hp_stored(self, strong_brick):
        assert strong_brick.max_hp == 3

    def test_brick_position(self, simple_brick):
        assert simple_brick.x == 100
        assert simple_brick.y == 50

    def test_brick_color(self, simple_brick):
        assert simple_brick.color == (255, 0, 0)

    def test_brick_get_rect(self, simple_brick):
        rect = simple_brick.get_rect()
        assert rect.x == 100
        assert rect.y == 50
        assert rect.width == 70
        assert rect.height == 22


# ── Brick hit / score tests ───────────────────────────────────────────────────

@pytest.mark.brick
class TestBrickHit:
    """Tests for Brick.hit() scoring and destruction."""

    @pytest.mark.parametrize("hp,expected_score", [
        (1, 10),
        (2, 20),
        (3, 30),
    ])
    def test_score_on_destroy(self, settings, hp, expected_score):
        brick = Brick(0, 0, (255, 0, 0), hp=hp)
        brick.width = settings.BRICK_WIDTH
        brick.height = settings.BRICK_HEIGHT
        # Hit until destroyed
        for _ in range(hp - 1):
            brick.hit()
        score = brick.hit()
        assert score == expected_score

    def test_single_hp_brick_dies_on_first_hit(self, simple_brick):
        simple_brick.hit()
        assert simple_brick.alive is False

    def test_multi_hp_brick_survives_partial_hits(self, strong_brick):
        strong_brick.hit()
        assert strong_brick.alive is True
        assert strong_brick.hp == 2

    def test_intermediate_hit_returns_zero(self, strong_brick):
        score = strong_brick.hit()
        assert score == 0

    def test_brick_not_alive_after_all_hp_removed(self, strong_brick):
        for _ in range(3):
            strong_brick.hit()
        assert strong_brick.alive is False

    def test_score_table_fallback_for_unknown_hp(self, settings):
        """Bricks with unknown max_hp return default score of 10."""
        brick = Brick(0, 0, (0, 0, 255), hp=5)
        brick.width = settings.BRICK_WIDTH
        brick.height = settings.BRICK_HEIGHT
        for _ in range(5):
            score = brick.hit()
        assert score == 10  # SCORE_TABLE fallback


# ── BrickGrid tests ───────────────────────────────────────────────────────────

@pytest.mark.brick_grid
class TestBrickGrid:
    """Tests for BrickGrid generation and state."""

    def test_correct_number_of_bricks(self, grid, settings):
        expected = settings.BRICK_ROWS * settings.BRICK_COLS
        assert len(grid.bricks) == expected

    def test_all_bricks_alive_at_start(self, grid):
        assert all(b.alive for b in grid.bricks)

    def test_alive_bricks_count_matches_total(self, grid, settings):
        assert len(grid.alive_bricks()) == settings.BRICK_ROWS * settings.BRICK_COLS

    def test_not_cleared_at_start(self, grid):
        assert grid.all_cleared() is False

    def test_all_cleared_when_all_dead(self, grid):
        for brick in grid.bricks:
            brick.alive = False
        assert grid.all_cleared() is True

    def test_alive_bricks_decreases_after_hit(self, grid, settings):
        total = settings.BRICK_ROWS * settings.BRICK_COLS
        # Kill one brick that has hp=1 (bottom rows)
        for brick in reversed(grid.bricks):
            if brick.hp == 1:
                brick.alive = False
                break
        assert len(grid.alive_bricks()) == total - 1

    def test_reset_restores_all_bricks(self, grid, settings):
        for brick in grid.bricks:
            brick.alive = False
        grid.reset()
        assert len(grid.alive_bricks()) == settings.BRICK_ROWS * settings.BRICK_COLS

    def test_top_rows_have_more_hp(self, grid):
        """First two rows (row < 2) should have hp == 3."""
        s = grid.settings
        top_count = s.BRICK_COLS * 2
        top_bricks = grid.bricks[:top_count]
        assert all(b.hp == 3 for b in top_bricks)

    def test_middle_rows_hp(self, grid):
        """Rows 2-3 should have hp == 2."""
        s = grid.settings
        mid_bricks = grid.bricks[s.BRICK_COLS * 2: s.BRICK_COLS * 4]
        assert all(b.hp == 2 for b in mid_bricks)

    def test_bottom_rows_hp(self, grid):
        """Rows 4+ should have hp == 1."""
        s = grid.settings
        bottom_bricks = grid.bricks[s.BRICK_COLS * 4:]
        assert all(b.hp == 1 for b in bottom_bricks)

    def test_brick_sizes_set_correctly(self, grid, settings):
        for brick in grid.bricks:
            assert brick.width == settings.BRICK_WIDTH
            assert brick.height == settings.BRICK_HEIGHT
