# UI: фон та сітка
# UI: HUD з очками та життями
# UI: стартовий екран
# UI: екран паузи
"""
UI module - HUD, menus, and all screen rendering
Author: Player2 (UI/Graphics)
"""

import pygame


class UI:
    """Handles all UI rendering: HUD, menus, overlays."""

    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self._load_fonts()

    def _load_fonts(self):
        pygame.font.init()
        self.font_large = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 28, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 20)
        self.font_tiny = pygame.font.SysFont("consolas", 15)

    def draw_background(self):
        self.screen.fill(self.settings.bg_color)
        # Subtle grid lines for depth
        grid_color = tuple(min(255, c + 12) for c in self.settings.bg_color)
        for x in range(0, self.settings.SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.settings.SCREEN_HEIGHT))
        for y in range(0, self.settings.SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.settings.SCREEN_WIDTH, y))

    def draw_hud(self, score, lives, level, difficulty):
        """Draw score, lives, level, and difficulty."""
        # Score
        score_surf = self.font_medium.render(f"SCORE: {score}", True, (255, 230, 100))
        self.screen.blit(score_surf, (10, 8))

        # Lives (hearts)
        heart_x = self.settings.SCREEN_WIDTH - 20
        for i in range(lives):
            heart_x -= 28
            pygame.draw.polygon(self.screen, (255, 60, 60), [
                (heart_x, 18), (heart_x - 8, 10), (heart_x - 12, 14),
                (heart_x - 8, 22), (heart_x, 28),
                (heart_x + 8, 22), (heart_x + 12, 14),
                (heart_x + 8, 10),
            ])

        # Level
        lvl_surf = self.font_small.render(f"LEVEL {level}", True, (160, 200, 255))
        self.screen.blit(lvl_surf, (self.settings.SCREEN_WIDTH // 2 - 35, 12))

        # Difficulty tag
        diff_colors = {"easy": (80, 220, 80), "medium": (255, 180, 50), "hard": (255, 60, 60)}
        diff_color = diff_colors.get(difficulty, (200, 200, 200))
        diff_surf = self.font_tiny.render(difficulty.upper(), True, diff_color)
        self.screen.blit(diff_surf, (self.settings.SCREEN_WIDTH // 2 - 20, 32))

        # Divider line
        pygame.draw.line(self.screen, (60, 60, 120),
                         (0, 48), (self.settings.SCREEN_WIDTH, 48), 2)

    def draw_launch_hint(self):
        hint = self.font_small.render("Press SPACE or click to launch", True, (180, 180, 180))
        rect = hint.get_rect(center=(self.settings.SCREEN_WIDTH // 2,
                                     self.settings.SCREEN_HEIGHT - 20))
        self.screen.blit(hint, rect)

    def draw_start_screen(self):
        self._draw_overlay(180)
        title = self.font_large.render("ARKANOID", True, (255, 230, 100))
        sub = self.font_medium.render("Press SPACE to Start", True, (180, 230, 255))
        controls = self.font_small.render("← → Arrow Keys or Mouse to move", True, (150, 150, 180))
        quit_hint = self.font_small.render("ESC to Quit", True, (120, 120, 150))

        cx = self.settings.SCREEN_WIDTH // 2
        cy = self.settings.SCREEN_HEIGHT // 2
        self.screen.blit(title, title.get_rect(center=(cx, cy - 80)))
        self.screen.blit(sub, sub.get_rect(center=(cx, cy)))
        self.screen.blit(controls, controls.get_rect(center=(cx, cy + 50)))
        self.screen.blit(quit_hint, quit_hint.get_rect(center=(cx, cy + 80)))

    def draw_pause_screen(self):
        self._draw_overlay(160)
        pause = self.font_large.render("PAUSED", True, (255, 230, 100))
        hint = self.font_medium.render("Press P to Resume", True, (180, 230, 255))
        cx = self.settings.SCREEN_WIDTH // 2
        cy = self.settings.SCREEN_HEIGHT // 2
        self.screen.blit(pause, pause.get_rect(center=(cx, cy - 30)))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 30)))

    def draw_game_over(self, score):
        self._draw_overlay(200)
        go = self.font_large.render("GAME OVER", True, (255, 60, 60))
        sc = self.font_medium.render(f"Final Score: {score}", True, (255, 230, 100))
        hint = self.font_small.render("Press R to Restart  |  ESC to Quit", True, (180, 180, 255))
        cx = self.settings.SCREEN_WIDTH // 2
        cy = self.settings.SCREEN_HEIGHT // 2
        self.screen.blit(go, go.get_rect(center=(cx, cy - 60)))
        self.screen.blit(sc, sc.get_rect(center=(cx, cy + 10)))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 60)))

    def draw_win(self, score):
        self._draw_overlay(200)
        win = self.font_large.render("YOU WIN!", True, (80, 255, 120))
        sc = self.font_medium.render(f"Score: {score}", True, (255, 230, 100))
        hint = self.font_small.render("Press R to Restart  |  ESC to Quit", True, (180, 180, 255))
        cx = self.settings.SCREEN_WIDTH // 2
        cy = self.settings.SCREEN_HEIGHT // 2
        self.screen.blit(win, win.get_rect(center=(cx, cy - 60)))
        self.screen.blit(sc, sc.get_rect(center=(cx, cy + 10)))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 60)))

    def draw_level_complete(self, level, score):
        self._draw_overlay(180)
        msg = self.font_large.render(f"LEVEL {level} CLEAR!", True, (100, 255, 180))
        sc = self.font_medium.render(f"Score: {score}", True, (255, 230, 100))
        hint = self.font_small.render("Press SPACE to continue", True, (180, 180, 255))
        cx = self.settings.SCREEN_WIDTH // 2
        cy = self.settings.SCREEN_HEIGHT // 2
        self.screen.blit(msg, msg.get_rect(center=(cx, cy - 50)))
        self.screen.blit(sc, sc.get_rect(center=(cx, cy + 20)))
        self.screen.blit(hint, hint.get_rect(center=(cx, cy + 70)))

    def _draw_overlay(self, alpha):
        overlay = pygame.Surface(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))
