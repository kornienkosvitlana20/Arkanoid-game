"""
Tests for Ball class (ball.py)
Author: Player 1 — Корнієнко Світлана
"""
import math
import pytest
import pygame
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ball import Ball
from settings import Settings

pygame.init()

# ── Фікстури ──────────────────────────────────────────────────────────────

@pytest.fixture
def settings():
    return Settings(difficulty="medium")


@pytest.fixture
def ball(settings):
    return Ball(settings)


@pytest.fixture
def active_ball(ball):
    """М'яч, який вже запущено."""
    ball.launch()
    return ball


# ── Маркери ───────────────────────────────────────────────────────────────

pytestmark = pytest.mark.ball  # всі тести цього файлу позначені маркером "ball"


# ── Тести початкового стану ───────────────────────────────────────────────

class TestBallInit:
    """Перевірка початкового стану після reset."""

    def test_ball_starts_inactive(self, ball):
        """М'яч після reset має бути неактивним."""
        assert ball.active is False

    def test_ball_starts_at_center_x(self, ball, settings):
        """М'яч має починатися по центру екрану по горизонталі."""
        assert ball.x == settings.SCREEN_WIDTH / 2

    def test_ball_velocity_upward_after_reset(self, ball):
        """Вертикальна швидкість після reset має бути від'ємною (вгору)."""
        assert ball.vy < 0

    def test_ball_radius_matches_settings(self, ball, settings):
        """Радіус м'яча має відповідати налаштуванням."""
        assert ball.radius == settings.BALL_RADIUS

    def test_ball_color_matches_settings(self, ball, settings):
        """Колір м'яча має відповідати налаштуванням."""
        assert ball.color == settings.BALL_COLOR


# ── Тести руху ────────────────────────────────────────────────────────────

class TestBallMovement:
    """Перевірка руху м'яча."""

    def test_inactive_ball_does_not_move(self, ball):
        """Неактивний м'яч не повинен рухатися."""
        x_before, y_before = ball.x, ball.y
        ball.update()
        assert ball.x == x_before
        assert ball.y == y_before

    def test_active_ball_moves(self, active_ball):
        """Активний м'яч повинен змінювати позицію після update."""
        x_before, y_before = active_ball.x, active_ball.y
        active_ball.update()
        assert active_ball.x != x_before or active_ball.y != y_before

    def test_launch_activates_ball(self, ball):
        """launch() має активувати м'яч."""
        ball.launch()
        assert ball.active is True


# ── Тести відбиття від стін ───────────────────────────────────────────────

class TestBallWallBounce:
    """Перевірка відбиття від меж екрану."""

    def test_bounce_off_left_wall(self, active_ball, settings):
        """М'яч повинен відбитися від лівої стіни (vx стає додатнім)."""
        active_ball.x = active_ball.radius - 1
        active_ball.vx = -5
        active_ball._bounce_walls()
        assert active_ball.vx > 0

    def test_bounce_off_right_wall(self, active_ball, settings):
        """М'яч повинен відбитися від правої стіни (vx стає від'ємним)."""
        active_ball.x = settings.SCREEN_WIDTH - active_ball.radius + 1
        active_ball.vx = 5
        active_ball._bounce_walls()
        assert active_ball.vx < 0

    def test_bounce_off_top_wall(self, active_ball):
        """М'яч повинен відбитися від верхньої стіни (vy стає додатнім)."""
        active_ball.y = active_ball.radius - 1
        active_ball.vy = -5
        active_ball._bounce_walls()
        assert active_ball.vy > 0

    def test_ball_position_corrected_on_left_wall(self, active_ball):
        """Позиція м'яча має бути скоригована щоб не виходити за ліву межу."""
        active_ball.x = -10
        active_ball.vx = -5
        active_ball._bounce_walls()
        assert active_ball.x >= active_ball.radius

    def test_no_bounce_in_free_space(self, active_ball, settings):
        """М'яч посередині екрану не повинен змінювати напрямок."""
        active_ball.x = settings.SCREEN_WIDTH / 2
        active_ball.y = settings.SCREEN_HEIGHT / 2
        vx_before = active_ball.vx
        vy_before = active_ball.vy
        active_ball._bounce_walls()
        assert active_ball.vx == vx_before
        assert active_ball.vy == vy_before


# ── Тести втрати м'яча ────────────────────────────────────────────────────

class TestBallLost:
    """Перевірка умови виходу м'яча за нижню межу."""

    def test_ball_lost_below_screen(self, ball, settings):
        """М'яч нижче екрану — is_lost() має повертати True."""
        ball.y = settings.SCREEN_HEIGHT + ball.radius + 1
        assert ball.is_lost() is True

    def test_ball_not_lost_on_screen(self, ball, settings):
        """М'яч на екрані — is_lost() має повертати False."""
        ball.y = settings.SCREEN_HEIGHT / 2
        assert ball.is_lost() is False

    def test_ball_not_lost_at_bottom_edge(self, ball, settings):
        """М'яч на нижньому краю екрану ще не вважається втраченим."""
        ball.y = settings.SCREEN_HEIGHT - ball.radius
        assert ball.is_lost() is False


# ── Тести колізії з платформою ────────────────────────────────────────────

class TestBallPaddleCollision:
    """Перевірка кутової колізії з платформою."""

    @pytest.fixture
    def paddle(self, settings):
        from paddle import Paddle
        return Paddle(settings)

    def test_ball_bounces_off_paddle(self, active_ball, paddle):
        """М'яч падає на платформу — vy має стати від'ємним (вгору)."""
        active_ball.x = paddle.x + paddle.width / 2
        active_ball.y = paddle.y - active_ball.radius + 1
        active_ball.vy = 5  # летить вниз

        active_ball.check_paddle_collision(paddle)

        assert active_ball.vy < 0

    def test_no_collision_when_ball_moving_up(self, active_ball, paddle):
        """Немає колізії, якщо м'яч рухається вгору."""
        active_ball.x = paddle.x + paddle.width / 2
        active_ball.y = paddle.y
        active_ball.vy = -5  # рухається вгору

        vy_before = active_ball.vy
        active_ball.check_paddle_collision(paddle)

        assert active_ball.vy == vy_before

    def test_inactive_ball_ignores_paddle(self, ball, paddle):
        """Неактивний м'яч не реагує на колізію з платформою."""
        ball.x = paddle.x + paddle.width / 2
        ball.y = paddle.y
        ball.vy = 5

        ball.check_paddle_collision(paddle)

        assert ball.vy == 5  # не змінилось

    @pytest.mark.parametrize("hit_pos_fraction,expected_vx_sign", [
        (0.1, -1),  # удар по лівому краю → м'яч летить вліво
        (0.9,  1),  # удар по правому краю → м'яч летить вправо
    ])
    def test_paddle_angle_reflection(self, active_ball, paddle,
                                     hit_pos_fraction, expected_vx_sign):
        """Кут відбиття залежить від місця удару по платформі."""
        active_ball.x = paddle.x + paddle.width * hit_pos_fraction
        active_ball.y = paddle.y - active_ball.radius + 1
        active_ball.vy = 5

        active_ball.check_paddle_collision(paddle)

        assert (active_ball.vx > 0) == (expected_vx_sign > 0)

    def test_ball_speed_increases_on_paddle_hit(self, active_ball, paddle, settings):
        """Швидкість м'яча збільшується після удару об платформу."""
        active_ball.x = paddle.x + paddle.width / 2
        active_ball.y = paddle.y - active_ball.radius + 1
        active_ball.vy = 5

        speed_before = math.hypot(active_ball.vx, active_ball.vy)
        active_ball.check_paddle_collision(paddle)
        speed_after = math.hypot(active_ball.vx, active_ball.vy)

        assert speed_after >= speed_before

    def test_ball_speed_capped_at_max(self, active_ball, paddle, settings):
        """Швидкість м'яча не перевищує max_ball_speed."""
        active_ball.x = paddle.x + paddle.width / 2
        active_ball.y = paddle.y - active_ball.radius + 1
        active_ball.vy = settings.max_ball_speed + 10

        active_ball.check_paddle_collision(paddle)
        speed = math.hypot(active_ball.vx, active_ball.vy)

        assert speed <= settings.max_ball_speed + 1  # +1 допуск на float


# ── Тести колізії з цеглинами ─────────────────────────────────────────────

class TestBallBrickCollision:
    """Перевірка колізії м'яча з цеглинами."""

    @pytest.fixture
    def brick(self):
        from brick import Brick
        b = Brick(100, 100, (255, 0, 0), hp=1)
        b.width = 70
        b.height = 22
        return b

    def test_collision_destroys_brick(self, active_ball, brick):
        """Зіткнення з цеглиною hp=1 знищує її."""
        active_ball.x = brick.x + brick.width / 2
        active_ball.y = brick.y + brick.height / 2

        active_ball.check_brick_collision([brick])

        assert brick.alive is False

    def test_collision_returns_score(self, active_ball, brick):
        """Знищення цеглини hp=1 повертає 10 очок."""
        active_ball.x = brick.x + brick.width / 2
        active_ball.y = brick.y + brick.height / 2

        score = active_ball.check_brick_collision([brick])

        assert score == 10

    def test_no_collision_with_dead_brick(self, active_ball, brick):
        """Мертва цеглина не враховується в колізії."""
        brick.alive = False
        active_ball.x = brick.x + brick.width / 2
        active_ball.y = brick.y + brick.height / 2

        score = active_ball.check_brick_collision([brick])

        assert score == 0

    def test_only_one_brick_per_frame(self, active_ball):
        """За один кадр м'яч б'ється лише об одну цеглину."""
        from brick import Brick
        bricks = []
        for i in range(3):
            b = Brick(100, 100, (255, 0, 0), hp=1)
            b.width = 70
            b.height = 22
            bricks.append(b)

        active_ball.x = 135
        active_ball.y = 111

        active_ball.check_brick_collision(bricks)

        destroyed = sum(1 for b in bricks if not b.alive)
        assert destroyed <= 1

    @pytest.mark.parametrize("hp,expected_score", [
        (1, 10),
        (2, 20),
        (3, 30),
    ])
    def test_score_by_brick_hp(self, active_ball, hp, expected_score):
        """Очки залежать від початкового HP цеглини."""
        from brick import Brick
        brick = Brick(100, 100, (200, 200, 200), hp=hp)
        brick.width = 70
        brick.height = 22

        # Б'ємо кілька разів щоб знищити
        for _ in range(hp):
            active_ball.x = brick.x + brick.width / 2
            active_ball.y = brick.y + brick.height / 2
            score = active_ball.check_brick_collision([brick])

        assert score == expected_score


# ── Тести малювання ───────────────────────────────────────────────────────

class TestBallDraw:
    """Перевірка методу draw (не викидає помилок)."""

    def test_draw_does_not_raise(self, ball):
        """draw() не повинен кидати виключень."""
        surface = pygame.Surface((800, 600))
        try:
            ball.draw(surface)
        except Exception as e:
            pytest.fail(f"draw() викинув виключення: {e}")
