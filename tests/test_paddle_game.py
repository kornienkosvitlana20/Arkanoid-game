"""
Tests for the Paddle class and Game state machine.
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

from paddle import Paddle
from settings import Settings
from game import Game, GameState


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings(difficulty="medium")


@pytest.fixture
def paddle(settings):
    return Paddle(settings)


@pytest.fixture
def game(settings):
    return Game(settings)


# ── Paddle tests ──────────────────────────────────────────────────────────────

@pytest.mark.paddle
class TestPaddleInit:
    """Tests for Paddle initialization."""

    def test_paddle_width(self, paddle, settings):
        assert paddle.width == settings.PADDLE_WIDTH

    def test_paddle_height(self, paddle, settings):
        assert paddle.height == settings.PADDLE_HEIGHT

    def test_paddle_centered_on_reset(self, paddle, settings):
        expected_x = (settings.SCREEN_WIDTH - settings.PADDLE_WIDTH) / 2
        assert paddle.x == expected_x

    def test_paddle_speed(self, paddle, settings):
        assert paddle.speed == settings.paddle_speed

    def test_paddle_get_rect(self, paddle):
        rect = paddle.get_rect()
        assert rect.width == paddle.width
        assert rect.height == paddle.height


@pytest.mark.paddle
class TestPaddleMovement:
    """Tests for Paddle movement boundaries."""

    def test_move_left_decreases_x(self, paddle):
        initial_x = paddle.x
        paddle.move_left()
        assert paddle.x < initial_x

    def test_move_right_increases_x(self, paddle):
        initial_x = paddle.x
        paddle.move_right()
        assert paddle.x > initial_x

    def test_cannot_move_left_past_zero(self, paddle):
        paddle.x = 0
        paddle.move_left()
        assert paddle.x == 0

    def test_cannot_move_right_past_screen(self, paddle, settings):
        paddle.x = settings.SCREEN_WIDTH - paddle.width
        paddle.move_right()
        assert paddle.x == settings.SCREEN_WIDTH - paddle.width

    def test_move_left_clamps_at_boundary(self, paddle):
        paddle.x = 2
        paddle.move_left()
        assert paddle.x == 0

    def test_reset_restores_center_position(self, paddle, settings):
        paddle.x = 0
        paddle.reset()
        expected_x = (settings.SCREEN_WIDTH - settings.PADDLE_WIDTH) / 2
        assert paddle.x == expected_x

    @pytest.mark.parametrize("start_x,expected_clamp", [
        (0, 0),
        (-10, 0),
    ])
    def test_move_left_boundary_parametrized(self, paddle, start_x, expected_clamp):
        paddle.x = start_x
        paddle.move_left()
        assert paddle.x >= expected_clamp


# ── Game state machine tests ──────────────────────────────────────────────────

@pytest.mark.game
class TestGameState:
    """Tests for Game state transitions."""

    def test_initial_state_is_start(self, game):
        assert game.state == GameState.START

    def test_initial_score_is_zero(self, game):
        assert game.score == 0

    def test_initial_lives(self, game, settings):
        assert game.lives == settings.lives

    def test_initial_level(self, game):
        assert game.level == 1

    def test_restart_resets_score(self, game):
        game.score = 500
        game._restart()
        assert game.score == 0

    def test_restart_resets_lives(self, game, settings):
        game.lives = 1
        game._restart()
        assert game.lives == settings.lives

    def test_restart_state_becomes_start(self, game):
        game.state = GameState.GAME_OVER
        game._restart()
        assert game.state == GameState.START

    def test_ball_lost_decrements_lives(self, game):
        initial_lives = game.lives
        game._on_ball_lost()
        assert game.lives == initial_lives - 1

    def test_ball_lost_with_lives_remaining_sets_ball_lost_state(self, game):
        game.lives = 2
        game._on_ball_lost()
        assert game.state == GameState.BALL_LOST

    def test_ball_lost_with_no_lives_sets_game_over(self, game):
        game.lives = 1
        game._on_ball_lost()
        assert game.state == GameState.GAME_OVER

    def test_level_complete_below_max_sets_level_complete(self, game):
        game.level = 1
        game._on_level_complete()
        assert game.state == GameState.LEVEL_COMPLETE

    def test_level_complete_at_max_sets_win(self, game):
        game.level = Game.MAX_LEVELS
        game._on_level_complete()
        assert game.state == GameState.WIN

    def test_next_level_increments_level(self, game):
        game.level = 1
        game._next_level()
        assert game.level == 2

    def test_next_level_sets_playing_state(self, game):
        game.level = 1
        game._next_level()
        assert game.state == GameState.PLAYING

    def test_respawn_ball_sets_playing_state(self, game):
        game.state = GameState.BALL_LOST
        game._respawn_ball()
        assert game.state == GameState.PLAYING


# ── Game mocking tests ────────────────────────────────────────────────────────

@pytest.mark.game
class TestGameMocking:
    """Tests using mocking for Game internals."""

    def test_score_increases_on_brick_collision(self, game, mocker):
        """Score should increase when ball destroys a brick."""
        mocker.patch.object(game.ball, 'update')
        mocker.patch.object(game.ball, 'check_paddle_collision')
        mocker.patch.object(game.ball, 'check_brick_collision', return_value=30)
        mocker.patch.object(game.ball, 'is_lost', return_value=False)
        mocker.patch.object(game.brick_grid, 'all_cleared', return_value=False)
        mocker.patch('pygame.key.get_pressed', return_value={
            pygame.K_LEFT: False, pygame.K_a: False,
            pygame.K_RIGHT: False, pygame.K_d: False,
        })
        mocker.patch('pygame.mouse.get_pos', return_value=(400, 500))

        game.state = GameState.PLAYING
        game._update()
        assert game.score == 30

    def test_on_ball_lost_called_when_ball_is_lost(self, game, mocker):
        """_on_ball_lost should be triggered when ball leaves screen."""
        mocker.patch.object(game.ball, 'update')
        mocker.patch.object(game.ball, 'check_paddle_collision')
        mocker.patch.object(game.ball, 'check_brick_collision', return_value=0)
        mocker.patch.object(game.ball, 'is_lost', return_value=True)
        mocker.patch.object(game.brick_grid, 'all_cleared', return_value=False)
        mocker.patch('pygame.key.get_pressed', return_value={
            pygame.K_LEFT: False, pygame.K_a: False,
            pygame.K_RIGHT: False, pygame.K_d: False,
        })
        mocker.patch('pygame.mouse.get_pos', return_value=(400, 500))

        mock_ball_lost = mocker.patch.object(game, '_on_ball_lost')
        game.state = GameState.PLAYING
        game._update()
        mock_ball_lost.assert_called_once()

    def test_level_complete_triggered_when_all_cleared(self, game, mocker):
        """_on_level_complete should fire when all bricks are cleared."""
        mocker.patch.object(game.ball, 'update')
        mocker.patch.object(game.ball, 'check_paddle_collision')
        mocker.patch.object(game.ball, 'check_brick_collision', return_value=0)
        mocker.patch.object(game.ball, 'is_lost', return_value=False)
        mocker.patch.object(game.brick_grid, 'all_cleared', return_value=True)
        mocker.patch('pygame.key.get_pressed', return_value={
            pygame.K_LEFT: False, pygame.K_a: False,
            pygame.K_RIGHT: False, pygame.K_d: False,
        })
        mocker.patch('pygame.mouse.get_pos', return_value=(400, 500))

        mock_level_complete = mocker.patch.object(game, '_on_level_complete')
        game.state = GameState.PLAYING
        game._update()
        mock_level_complete.assert_called_once()

    def test_update_does_nothing_when_not_playing(self, game, mocker):
        """_update should be a no-op unless state == PLAYING."""
        mock_ball_update = mocker.patch.object(game.ball, 'update')
        game.state = GameState.PAUSED
        game._update()
        mock_ball_update.assert_not_called()

    def test_ball_speed_increases_on_next_level(self, game, mocker):
        """Ball speed should increment when advancing to next level."""
        mocker.patch.object(game.ball, 'reset')
        mocker.patch.object(game.ball, 'launch')
        mocker.patch.object(game.paddle, 'reset')
        mocker.patch.object(game.brick_grid, 'reset')

        initial_speed = game.settings.ball_speed
        game.level = 1
        game._next_level()
        assert game.settings.ball_speed == min(
            initial_speed + 1, game.settings.max_ball_speed
        )
