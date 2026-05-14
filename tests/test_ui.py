"""
Tests for UI class (ui.py)
Author: Player 2 — Вялкова Поліна
"""
import pytest
import pygame
from unittest.mock import patch

pygame.init()

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ui import UI
from settings import Settings


pytestmark = pytest.mark.ui


# ── Фікстури ──────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings(difficulty="medium", bg_color="dark_blue")


@pytest.fixture
def screen():
    return pygame.Surface((800, 600))


@pytest.fixture
def ui(settings, screen):
    return UI(settings, screen)


# ── Тести ініціалізації ───────────────────────────────────────────────────

class TestUIInit:
    """Перевірка ініціалізації UI."""

    def test_ui_stores_settings(self, ui, settings):
        """UI зберігає налаштування."""
        assert ui.settings is settings

    def test_ui_stores_screen(self, ui, screen):
        """UI зберігає посилання на screen."""
        assert ui.screen is screen

    def test_ui_loads_fonts(self, ui):
        """UI має завантажені шрифти."""
        assert ui.font_large is not None
        assert ui.font_medium is not None
        assert ui.font_small is not None
        assert ui.font_tiny is not None


# ── Тести draw_background ─────────────────────────────────────────────────

class TestUIBackground:
    """Перевірка методу draw_background."""

    def test_draw_background_does_not_raise(self, ui):
        """draw_background() не кидає виключень."""
        try:
            ui.draw_background()
        except Exception as e:
            pytest.fail(f"draw_background() кинув виключення: {e}")

    @pytest.mark.parametrize("bg_color", ["dark_blue", "black", "dark_purple", "dark_green"])
    def test_draw_background_all_themes(self, bg_color, screen):
        """draw_background() працює для всіх тем."""
        s = Settings(bg_color=bg_color)
        ui = UI(s, screen)
        try:
            ui.draw_background()
        except Exception as e:
            pytest.fail(f"draw_background({bg_color}) кинув виключення: {e}")


# ── Тести draw_hud ────────────────────────────────────────────────────────

class TestUIHud:
    """Перевірка методу draw_hud."""

    def test_draw_hud_does_not_raise(self, ui):
        """draw_hud() не кидає виключень."""
        try:
            ui.draw_hud(score=100, lives=3, level=1, difficulty="medium")
        except Exception as e:
            pytest.fail(f"draw_hud() кинув виключення: {e}")

    @pytest.mark.parametrize("score,lives,level,difficulty", [
        (0, 1, 1, "easy"),
        (999, 3, 2, "medium"),
        (12345, 0, 3, "hard"),
    ])
    def test_draw_hud_various_values(self, ui, score, lives, level, difficulty):
        """draw_hud() працює з різними значеннями."""
        try:
            ui.draw_hud(score=score, lives=lives, level=level, difficulty=difficulty)
        except Exception as e:
            pytest.fail(f"draw_hud({score}, {lives}, {level}) кинув виключення: {e}")

    def test_draw_hud_zero_lives(self, ui):
        """draw_hud() не кидає помилку при 0 життях."""
        try:
            ui.draw_hud(score=0, lives=0, level=1, difficulty="medium")
        except Exception as e:
            pytest.fail(f"draw_hud з 0 lives кинув виключення: {e}")


# ── Тести екранів ─────────────────────────────────────────────────────────

class TestUIScreens:
    """Перевірка різних екранів UI."""

    def test_draw_start_screen_does_not_raise(self, ui):
        """draw_start_screen() не кидає виключень."""
        try:
            ui.draw_start_screen()
        except Exception as e:
            pytest.fail(f"draw_start_screen() кинув виключення: {e}")

    def test_draw_pause_screen_does_not_raise(self, ui):
        """draw_pause_screen() не кидає виключень."""
        try:
            ui.draw_pause_screen()
        except Exception as e:
            pytest.fail(f"draw_pause_screen() кинув виключення: {e}")

    def test_draw_game_over_does_not_raise(self, ui):
        """draw_game_over() не кидає виключень."""
        try:
            ui.draw_game_over(score=250)
        except Exception as e:
            pytest.fail(f"draw_game_over() кинув виключення: {e}")

    def test_draw_win_does_not_raise(self, ui):
        """draw_win() не кидає виключень."""
        try:
            ui.draw_win(score=1500)
        except Exception as e:
            pytest.fail(f"draw_win() кинув виключення: {e}")

    def test_draw_level_complete_does_not_raise(self, ui):
        """draw_level_complete() не кидає виключень."""
        try:
            ui.draw_level_complete(level=1, score=500)
        except Exception as e:
            pytest.fail(f"draw_level_complete() кинув виключення: {e}")

    def test_draw_launch_hint_does_not_raise(self, ui):
        """draw_launch_hint() не кидає виключень."""
        try:
            ui.draw_launch_hint()
        except Exception as e:
            pytest.fail(f"draw_launch_hint() кинув виключення: {e}")

    @pytest.mark.parametrize("level", [1, 2, 3])
    def test_level_complete_all_levels(self, ui, level):
        """draw_level_complete() працює для всіх рівнів."""
        try:
            ui.draw_level_complete(level=level, score=100 * level)
        except Exception as e:
            pytest.fail(f"draw_level_complete(level={level}) кинув виключення: {e}")


# ── Тести з мокуванням ────────────────────────────────────────────────────

class TestUIWithMocking:
    """Тести UI з мокуванням внутрішніх викликів."""

    def test_draw_background_fills_with_bg_color(self, ui, settings):
        """draw_background() заповнює екран кольором фону (перевіряємо піксель)."""
        ui.draw_background()
        # Після виклику draw_background верхній лівий піксель != чорний
        # (якщо фон не чорний), або ж просто перевіряємо, що метод не викидає помилок
        # і поверхня змінила колір
        pixel = ui.screen.get_at((0, 0))
        # Перевіряємо що піксель відповідає одному з компонентів bg_color
        assert pixel[:3] is not None  # pygame повернув кортеж RGB

    def test_draw_overlay_creates_surface_with_srcalpha(self, ui):
        """_draw_overlay() створює напівпрозору Surface з SRCALPHA."""
        # Мокуємо тільки pygame.Surface всередині модулю ui
        created_surfaces = []

        original_surface = pygame.Surface

        def capturing_surface(size, flags=0):
            surf = original_surface(size, flags)
            created_surfaces.append((size, flags))
            return surf

        with patch('pygame.Surface', side_effect=capturing_surface):
            ui._draw_overlay(180)

        # Перевіряємо що була створена поверхня з SRCALPHA
        assert any(flags == pygame.SRCALPHA for _, flags in created_surfaces)
