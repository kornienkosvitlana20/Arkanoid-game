"""
Tests for Settings class (settings.py)
Author: Player 2 — Вялкова Поліна
"""
import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from settings import Settings, BG_COLORS


pytestmark = pytest.mark.settings


# ── Тести ініціалізації ───────────────────────────────────────────────────

class TestSettingsInit:
    """Перевірка ініціалізації налаштувань."""

    def test_default_difficulty_is_medium(self):
        """За замовчуванням — medium складність."""
        s = Settings()
        assert s.difficulty == "medium"

    def test_custom_difficulty_stored(self):
        """Вибрана складність зберігається."""
        s = Settings(difficulty="hard")
        assert s.difficulty == "hard"

    def test_custom_lives_stored(self):
        """Кількість життів зберігається."""
        s = Settings(lives=5)
        assert s.lives == 5

    def test_default_lives(self):
        """За замовчуванням 3 життя."""
        s = Settings()
        assert s.lives == 3

    def test_screen_dimensions(self):
        """Розміри екрану визначені."""
        assert Settings.SCREEN_WIDTH == 800
        assert Settings.SCREEN_HEIGHT == 600

    def test_fps_defined(self):
        """FPS визначено."""
        assert Settings.FPS == 60

    def test_title_defined(self):
        """Назва гри визначена."""
        assert Settings.TITLE == "Arkanoid"


# ── Тести складності ──────────────────────────────────────────────────────

class TestDifficultySettings:
    """Перевірка налаштувань складності."""

    @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
    def test_all_difficulties_exist(self, difficulty):
        """Всі рівні складності мають бути визначені."""
        s = Settings(difficulty=difficulty)
        assert s.ball_speed > 0

    def test_easy_slower_than_hard(self):
        """Easy повільніше ніж hard."""
        easy = Settings(difficulty="easy")
        hard = Settings(difficulty="hard")
        assert easy.ball_speed < hard.ball_speed

    def test_easy_paddle_slower_than_hard(self):
        """Платформа на easy повільніша ніж на hard."""
        easy = Settings(difficulty="easy")
        hard = Settings(difficulty="hard")
        assert easy.paddle_speed < hard.paddle_speed

    def test_max_speed_increases_with_difficulty(self):
        """Максимальна швидкість зростає зі складністю."""
        easy = Settings(difficulty="easy")
        medium = Settings(difficulty="medium")
        hard = Settings(difficulty="hard")
        assert easy.max_ball_speed < medium.max_ball_speed < hard.max_ball_speed

    @pytest.mark.parametrize("difficulty,expected_speed", [
        ("easy",   5),
        ("medium", 7),
        ("hard",   9),
    ])
    def test_ball_speed_by_difficulty(self, difficulty, expected_speed):
        """Швидкість м'яча відповідає очікуваній для кожної складності."""
        s = Settings(difficulty=difficulty)
        assert s.ball_speed == expected_speed

    @pytest.mark.parametrize("difficulty,expected_max", [
        ("easy",   10),
        ("medium", 14),
        ("hard",   18),
    ])
    def test_max_ball_speed_by_difficulty(self, difficulty, expected_max):
        """Максимальна швидкість відповідає очікуваній для кожної складності."""
        s = Settings(difficulty=difficulty)
        assert s.max_ball_speed == expected_max


# ── Тести кольорів фону ───────────────────────────────────────────────────

class TestBackgroundColors:
    """Перевірка кольорів фону."""

    @pytest.mark.parametrize("bg_name", ["dark_blue", "black", "dark_purple", "dark_green"])
    def test_all_bg_colors_available(self, bg_name):
        """Всі теми фону мають бути доступні."""
        s = Settings(bg_color=bg_name)
        assert s.bg_color is not None

    def test_unknown_bg_falls_back_to_dark_blue(self):
        """Невідомий колір фону → повертається dark_blue."""
        s = Settings(bg_color="nonexistent_color")
        assert s.bg_color == BG_COLORS["dark_blue"]

    def test_bg_color_is_tuple(self):
        """Колір фону — кортеж RGB."""
        s = Settings(bg_color="dark_blue")
        assert isinstance(s.bg_color, tuple)
        assert len(s.bg_color) == 3

    def test_black_bg_is_black(self):
        """Чорний фон = (0, 0, 0)."""
        s = Settings(bg_color="black")
        assert s.bg_color == (0, 0, 0)


# ── Тести констант цеглин ─────────────────────────────────────────────────

class TestBrickConstants:
    """Перевірка констант сітки цеглин."""

    def test_brick_rows_defined(self):
        """BRICK_ROWS визначено."""
        assert Settings.BRICK_ROWS == 6

    def test_brick_cols_defined(self):
        """BRICK_COLS визначено."""
        assert Settings.BRICK_COLS == 10

    def test_brick_colors_count(self):
        """Кількість кольорів цеглин = кількість рядів."""
        assert len(Settings.BRICK_COLORS) == Settings.BRICK_ROWS

    def test_brick_colors_are_rgb_tuples(self):
        """Кожен колір цеглини — кортеж з 3 значень."""
        for color in Settings.BRICK_COLORS:
            assert len(color) == 3
            assert all(0 <= c <= 255 for c in color)

    def test_brick_dimensions_positive(self):
        """Розміри цеглин мають бути додатніми."""
        assert Settings.BRICK_WIDTH > 0
        assert Settings.BRICK_HEIGHT > 0
        assert Settings.BRICK_PADDING >= 0
