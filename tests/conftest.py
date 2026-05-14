"""
Shared pytest fixtures for Arkanoid test suite.
"""
import sys
import os
import pytest

# Дозволяємо імпортувати модулі з src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
pygame.init()
# Створюємо мінімальне вікно для тестів (без відображення)
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')


from settings import Settings


@pytest.fixture
def settings():
    """Default medium-difficulty settings."""
    return Settings(difficulty="medium", bg_color="dark_blue", lives=3)


@pytest.fixture
def settings_easy():
    """Easy difficulty settings."""
    return Settings(difficulty="easy", bg_color="dark_blue", lives=5)


@pytest.fixture
def settings_hard():
    """Hard difficulty settings."""
    return Settings(difficulty="hard", bg_color="dark_blue", lives=1)


@pytest.fixture
def ball(settings):
    """A fresh Ball instance."""
    from ball import Ball
    return Ball(settings)


@pytest.fixture
def paddle(settings):
    """A fresh Paddle instance."""
    from paddle import Paddle
    return Paddle(settings)


@pytest.fixture
def brick_grid(settings):
    """A fresh BrickGrid instance."""
    from brick_grid import BrickGrid
    return BrickGrid(settings)


@pytest.fixture
def surface():
    """A pygame surface for draw tests."""
    return pygame.Surface((800, 600))
