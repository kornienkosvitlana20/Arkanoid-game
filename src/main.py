# Головний файл: argparse аргументи
"""
Arkanoid Game - Main Entry Point
Author: Team (Player1 - Game Logic, Player2 - UI/Graphics)
"""

import pygame
import argparse
import sys
from game import Game
from settings import Settings


def parse_args():
    parser = argparse.ArgumentParser(description="Arkanoid Game")
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        default="medium",
        help="Game difficulty level (default: medium)"
    )
    parser.add_argument(
        "--bg-color",
        default="dark_blue",
        choices=["dark_blue", "black", "dark_purple", "dark_green"],
        help="Background color theme (default: dark_blue)"
    )
    parser.add_argument(
        "--lives",
        type=int,
        default=3,
        choices=[1, 2, 3, 5],
        help="Number of lives (default: 3)"
    )
    parser.add_argument(
        "--fullscreen",
        action="store_true",
        help="Run in fullscreen mode"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    pygame.init()
    pygame.mixer.init()

    settings = Settings(
        difficulty=args.difficulty,
        bg_color=args.bg_color,
        lives=args.lives,
        fullscreen=args.fullscreen
    )

    game = Game(settings)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
