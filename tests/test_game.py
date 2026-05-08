"""
Tests for Game / GameState (game.py)
Author: Player 1 — Корнієнко Світлана
"""
import pytest
import pygame
from unittest.mock import MagicMock, patch

pygame.init()

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from settings import Settings
from game import Game, GameState


pytestmark = pytest.mark.game


# ── Фікстури ──────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings(difficulty="medium", lives=3)


@pytest.fixture
def game(settings):
    """Створює Game з мокованим дисплеєм."""
    pygame.display.set_mode((800, 600))
    g = Game(settings)
    return g


# ── Тести GameState ───────────────────────────────────────────────────────

class TestGameState:
    """Перевірка констант GameState."""

    def test_state_values_exist(self):
        """Всі стани мають бути визначені."""
        assert hasattr(GameState, 'START')
        assert hasattr(GameState, 'PLAYING')
        assert hasattr(GameState, 'PAUSED')
        assert hasattr(GameState, 'BALL_LOST')
        assert hasattr(GameState, 'LEVEL_COMPLETE')
        assert hasattr(GameState, 'GAME_OVER')
        assert hasattr(GameState, 'WIN')

    def test_state_values_are_strings(self):
        """Стани мають бути рядками."""
        assert isinstance(GameState.START, str)
        assert isinstance(GameState.PLAYING, str)

    def test_states_are_unique(self):
        """Всі значення станів мають бути унікальними."""
        states = [
            GameState.START, GameState.PLAYING, GameState.PAUSED,
            GameState.BALL_LOST, GameState.LEVEL_COMPLETE,
            GameState.GAME_OVER, GameState.WIN,
        ]
        assert len(states) == len(set(states))


# ── Тести ініціалізації Game ──────────────────────────────────────────────

class TestGameInit:
    """Перевірка початкового стану гри."""

    def test_game_starts_in_start_state(self, game):
        """Гра має починатися зі стану START."""
        assert game.state == GameState.START

    def test_initial_score_is_zero(self, game):
        """Початковий рахунок = 0."""
        assert game.score == 0

    def test_initial_lives(self, game, settings):
        """Початкова кількість життів береться з settings."""
        assert game.lives == settings.lives

    def test_initial_level_is_one(self, game):
        """Початковий рівень = 1."""
        assert game.level == 1

    def test_game_has_all_components(self, game):
        """Гра має всі необхідні компоненти."""
        assert game.ball is not None
        assert game.paddle is not None
        assert game.brick_grid is not None
        assert game.ui is not None


# ── Тести втрати м'яча ────────────────────────────────────────────────────

class TestBallLostLogic:
    """Перевірка логіки при втраті м'яча."""

    def test_life_lost_when_ball_falls(self, game):
        """Втрата м'яча зменшує кількість життів на 1."""
        lives_before = game.lives
        game._on_ball_lost()
        assert game.lives == lives_before - 1

    def test_state_becomes_ball_lost_with_lives(self, game):
        """При залишкових життях стан → BALL_LOST."""
        game.lives = 2
        game._on_ball_lost()
        assert game.state == GameState.BALL_LOST

    def test_state_becomes_game_over_no_lives(self, game):
        """При 0 життях після втрати → GAME_OVER."""
        game.lives = 1
        game._on_ball_lost()
        assert game.state == GameState.GAME_OVER

    def test_ball_resets_on_ball_lost(self, game):
        """М'яч скидається після втрати."""
        game.lives = 2
        game.ball.active = True
        game._on_ball_lost()
        assert game.ball.active is False

    def test_paddle_resets_on_ball_lost(self, game, settings):
        """Платформа повертається до центру після втрати м'яча."""
        game.lives = 2
        game.paddle.x = 0  # зміщуємо платформу
        game._on_ball_lost()
        expected_x = (settings.SCREEN_WIDTH - settings.PADDLE_WIDTH) / 2
        assert game.paddle.x == expected_x


# ── Тести завершення рівня ────────────────────────────────────────────────

class TestLevelComplete:
    """Перевірка логіки завершення рівня."""

    def test_level_complete_before_max(self, game):
        """Якщо рівень < MAX → стан LEVEL_COMPLETE."""
        game.level = 1
        game._on_level_complete()
        assert game.state == GameState.LEVEL_COMPLETE

    def test_win_state_on_last_level(self, game):
        """Якщо пройдено всі рівні → стан WIN."""
        game.level = Game.MAX_LEVELS
        game._on_level_complete()
        assert game.state == GameState.WIN

    def test_next_level_increments_level(self, game):
        """_next_level() збільшує лічильник рівнів."""
        game.level = 1
        game._next_level()
        assert game.level == 2

    def test_next_level_resets_bricks(self, game):
        """_next_level() відновлює сітку цеглин."""
        for brick in game.brick_grid.bricks:
            brick.alive = False
        game._next_level()
        assert not game.brick_grid.all_cleared()

    def test_next_level_increases_ball_speed(self, game, settings):
        """_next_level() збільшує швидкість м'яча."""
        speed_before = settings.ball_speed
        game._next_level()
        assert settings.ball_speed > speed_before

    def test_ball_speed_capped_on_next_level(self, game, settings):
        """Швидкість м'яча не перевищує max при переході рівня."""
        settings.ball_speed = settings.max_ball_speed
        game._next_level()
        assert settings.ball_speed <= settings.max_ball_speed


# ── Тести рестарту ────────────────────────────────────────────────────────

class TestGameRestart:
    """Перевірка методу _restart."""

    def test_restart_resets_score(self, game):
        """_restart() скидає рахунок до 0."""
        game.score = 999
        game._restart()
        assert game.score == 0

    def test_restart_resets_level(self, game):
        """_restart() скидає рівень до 1."""
        game.level = 3
        game._restart()
        assert game.level == 1

    def test_restart_resets_lives(self, game, settings):
        """_restart() відновлює кількість життів."""
        game.lives = 0
        game._restart()
        assert game.lives == settings.lives

    def test_restart_sets_start_state(self, game):
        """_restart() переводить гру в стан START."""
        game.state = GameState.GAME_OVER
        game._restart()
        assert game.state == GameState.START


# ── Тести з мокуванням ────────────────────────────────────────────────────

class TestGameWithMocking:
    """Тести з використанням mock-об'єктів."""

    def test_score_incremented_on_brick_hit(self, game):
        """Рахунок збільшується коли м'яч б'є по цеглині."""
        game.state = GameState.PLAYING
        game.ball.active = True

        # Мокуємо check_brick_collision щоб повертав 10 очок
        game.ball.check_brick_collision = MagicMock(return_value=10)
        game.ball.update = MagicMock()
        game.ball.check_paddle_collision = MagicMock()
        game.ball.is_lost = MagicMock(return_value=False)
        game.brick_grid.all_cleared = MagicMock(return_value=False)

        game._update()

        assert game.score == 10

    def test_on_ball_lost_called_when_ball_falls(self, game):
        """_on_ball_lost() викликається коли м'яч падає за екран."""
        game.state = GameState.PLAYING
        game.ball.active = True
        game.ball.update = MagicMock()
        game.ball.check_paddle_collision = MagicMock()
        game.ball.check_brick_collision = MagicMock(return_value=0)
        game.ball.is_lost = MagicMock(return_value=True)
        game.brick_grid.all_cleared = MagicMock(return_value=False)

        with patch.object(game, '_on_ball_lost') as mock_lost:
            game._update()
            mock_lost.assert_called_once()

    def test_level_complete_called_when_all_cleared(self, game):
        """_on_level_complete() викликається коли всі цеглини знищені."""
        game.state = GameState.PLAYING
        game.ball.update = MagicMock()
        game.ball.check_paddle_collision = MagicMock()
        game.ball.check_brick_collision = MagicMock(return_value=0)
        game.ball.is_lost = MagicMock(return_value=False)
        game.brick_grid.all_cleared = MagicMock(return_value=True)

        with patch.object(game, '_on_level_complete') as mock_complete:
            game._update()
            mock_complete.assert_called_once()

    def test_update_does_nothing_when_paused(self, game):
        """_update() нічого не робить у стані PAUSED."""
        game.state = GameState.PAUSED
        score_before = game.score

        game.ball.update = MagicMock()
        game._update()

        game.ball.update.assert_not_called()
        assert game.score == score_before
