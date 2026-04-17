# М'яч: ефект світіння
"""
Ball module - ball physics and collision logic
Author: Player1 (Game Logic)
"""

import pygame
import math
import random

# Ball: handles movement and physics
class Ball:
    """Represents the game ball with physics."""

    def __init__(self, settings):
        self.settings = settings
        self.radius = settings.BALL_RADIUS
        self.color = settings.BALL_COLOR
        self.reset()

    def reset(self):
        """Reset ball to starting position above paddle."""
        self.x = self.settings.SCREEN_WIDTH / 2
        self.y = self.settings.SCREEN_HEIGHT - self.settings.PADDLE_Y_OFFSET - self.settings.PADDLE_HEIGHT - self.radius - 5
        angle = random.uniform(math.radians(210), math.radians(330))
        speed = self.settings.ball_speed
        self.vx = speed * math.cos(angle)
        self.vy = -abs(speed * math.sin(angle))
        self.active = False  # ball waits for launch

    def launch(self):
        self.active = True

    def update(self):
        if not self.active:
            return
        self.x += self.vx
        self.y += self.vy
        self._bounce_walls()

    def _bounce_walls(self):
        """Bounce off left, right, and top walls."""
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius >= self.settings.SCREEN_WIDTH:
            self.x = self.settings.SCREEN_WIDTH - self.radius
            self.vx = -abs(self.vx)
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = abs(self.vy)

    def is_lost(self):
        """Check if ball fell below screen."""
        return self.y - self.radius > self.settings.SCREEN_HEIGHT

    # angle-based paddle collision
    def check_paddle_collision(self, paddle):
        """Handle collision with paddle with angle reflection."""
        if not self.active:
            return
        paddle_rect = paddle.get_rect()
        ball_rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius,
            self.radius * 2, self.radius * 2
        )
        if ball_rect.colliderect(paddle_rect) and self.vy > 0:
            # Reflect based on hit position on paddle
            hit_pos = (self.x - paddle.x) / paddle.width  # 0.0 to 1.0
            angle = math.radians(150 + hit_pos * (-120))  # 150° to 30°
            speed = min(
                math.hypot(self.vx, self.vy) + self.settings.ball_speed_increment,
                self.settings.max_ball_speed
            )
            self.vx = speed * math.cos(angle)
            self.vy = -abs(speed * math.sin(angle))
            self.y = paddle_rect.top - self.radius

    def check_brick_collision(self, bricks):
        """Check collision with bricks. Returns score gained."""
        score = 0
        ball_rect = pygame.Rect(
            self.x - self.radius, self.y - self.radius,
            self.radius * 2, self.radius * 2
        )
        for brick in bricks[:]:
            if not brick.alive:
                continue
            if ball_rect.colliderect(brick.get_rect()):
                score += brick.hit()
                self._reflect_off_brick(brick)
                break  # one brick per frame
        return score

    def _reflect_off_brick(self, brick):
        """Reflect ball based on which side of brick was hit."""
        brect = brick.get_rect()
        # Determine overlap on each axis
        dx = min(self.x - brect.left, brect.right - self.x)
        dy = min(self.y - brect.top, brect.bottom - self.y)
        if dx < dy:
            self.vx = -self.vx
        else:
            self.vy = -self.vy

    def draw(self, surface):
        """Draw the ball with a glow effect."""
        # Glow
        glow_surf = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color[:3], 40),
                           (self.radius * 3, self.radius * 3), self.radius * 3)
        surface.blit(glow_surf, (int(self.x) - self.radius * 3, int(self.y) - self.radius * 3))
        # Ball
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Shine
        pygame.draw.circle(surface, (255, 255, 255),
                           (int(self.x) - self.radius // 3, int(self.y) - self.radius // 3),
                           self.radius // 3)
