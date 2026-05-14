"""
conftest.py – shared fixtures and pytest configuration.
"""
import sys
import os

# Ensure src/ is on the path for all test modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')


def pytest_configure(config):
    """Initialize pygame once before the test session."""
    pygame.init()
    pygame.display.set_mode((800, 600))


def pytest_unconfigure(config):
    pygame.quit()
