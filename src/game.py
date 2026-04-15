"""
Game module - main game loop and state management
Author: Player1 (Game Logic) + Player2 (UI integration)
"""

import pygame
import sys
from settings import Settings
from ball import Ball
from paddle import Paddle
from brick_grid import BrickGrid
from ui import UI

# scoring system
class GameState:
    START = "start"
    PLAYING = "playing"
    PAUSED = "paused"
    BALL_LOST = "ball_lost"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    WIN = "win"


class Game:
    """Main game controller - manages state, loop, events."""

    MAX_LEVELS = 3

    def __init__(self, settings: Settings):
        self.settings = settings

        flags = pygame.FULLSCREEN if settings.fullscreen else 0
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), flags
        )
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()

        self.ui = UI(settings, self.screen)
        self._init_game_objects()
        self.state = GameState.START

    def _init_game_objects(self):
        self.paddle = Paddle(self.settings)
        self.ball = Ball(self.settings)
        self.brick_grid = BrickGrid(self.settings)
        self.score = 0
        self.lives = self.settings.lives
        self.level = 1

    def run(self):
        """Main game loop."""
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(self.settings.FPS)

    # ── Event handling ──────────────────────────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self._handle_keydown(event)
            self._handle_mouse(event)

    def _handle_keydown(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if self.state == GameState.START:
            if event.key == pygame.K_SPACE:
                self.state = GameState.PLAYING
                self.ball.launch()

        elif self.state == GameState.PLAYING:
            if event.key == pygame.K_p:
                self.state = GameState.PAUSED
            if event.key == pygame.K_SPACE:
                self.ball.launch()

        elif self.state == GameState.PAUSED:
            if event.key == pygame.K_p:
                self.state = GameState.PLAYING

        elif self.state in (GameState.GAME_OVER, GameState.WIN):
            if event.key == pygame.K_r:
                self._restart()

        elif self.state == GameState.LEVEL_COMPLETE:
            if event.key == pygame.K_SPACE:
                self._next_level()

        elif self.state == GameState.BALL_LOST:
            if event.key == pygame.K_SPACE:
                self._respawn_ball()

    def _handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.state == GameState.PLAYING:
            self.ball.launch()

    # ── Update ──────────────────────────────────────────────────────────────

    def _update(self):
        if self.state != GameState.PLAYING:
            return

        self._move_paddle()
        self.ball.update()
        self.ball.check_paddle_collision(self.paddle)
        gained = self.ball.check_brick_collision(self.brick_grid.bricks)
        self.score += gained

        if self.ball.is_lost():
            self._on_ball_lost()

        if self.brick_grid.all_cleared():
            self._on_level_complete()

    def _move_paddle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move_right()
        # Mouse control
        mx, _ = pygame.mouse.get_pos()
        self.paddle.x = max(0, min(self.settings.SCREEN_WIDTH - self.paddle.width,
                                   mx - self.paddle.width // 2))

    def _on_ball_lost(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
        else:
            self.state = GameState.BALL_LOST
            self.ball.reset()
            self.paddle.reset()

    def _on_level_complete(self):
        if self.level >= self.MAX_LEVELS:
            self.state = GameState.WIN
        else:
            self.state = GameState.LEVEL_COMPLETE

    def _next_level(self):
        self.level += 1
        self.brick_grid.reset()
        self.ball.reset()
        self.paddle.reset()
        # Speed up ball for next level
        self.settings.ball_speed = min(
            self.settings.ball_speed + 1,
            self.settings.max_ball_speed
        )
        self.state = GameState.PLAYING
        self.ball.launch()

    def _respawn_ball(self):
        self.state = GameState.PLAYING

    def _restart(self):
        self._init_game_objects()
        self.state = GameState.START

    # ── Draw ────────────────────────────────────────────────────────────────

    def _draw(self):
        self.ui.draw_background()
        self.brick_grid.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.ui.draw_hud(self.score, self.lives, self.level, self.settings.difficulty)

        if self.state == GameState.START:
            self.ui.draw_start_screen()
        elif self.state == GameState.PAUSED:
            self.ui.draw_pause_screen()
        elif self.state == GameState.BALL_LOST:
            self.ui.draw_launch_hint()
        elif self.state == GameState.LEVEL_COMPLETE:
            self.ui.draw_level_complete(self.level, self.score)
        elif self.state == GameState.GAME_OVER:
            self.ui.draw_game_over(self.score)
        elif self.state == GameState.WIN:
            self.ui.draw_win(self.score)

        pygame.display.flip()
