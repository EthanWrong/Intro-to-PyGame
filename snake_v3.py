"""Snake - v3
- restructured everything to be more organised
by Ethan Wong"""

import pygame
import time

pygame.init()


# Class to handle the game's rendering
class Screen:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size

        # Initialise screen
        self.GAME_ICON = pygame.image.load('Images/snake_icon.png')
        pygame.display.set_icon(self.GAME_ICON)
        pygame.display.set_caption("Snake game - by Ethan Wong")
        self.SCREEN = pygame.display.set_mode((width * block_size, height * block_size))

        # Initialise colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Import fonts
        self.FONT1 = pygame.font.SysFont("arialblack", 20)
        self.FONT2 = pygame.font.SysFont("consolas", 30)


class Player:
    def __init__(self, highscore=0):
        self.grid = [  # x, y
            [3, 1],
            [2, 1],
            [1, 1]
        ]
        self.score = 0
        self.direction = "right"
        self.alive = True
        self.highscore = highscore


# Class to handle the game's logic
class Main:
    def __init__(self, cols, rows, block_size):
        self.cols = cols
        self.rows = rows
        self.block_size = block_size

        # Initialise grid, in which the game logic will be done
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.screen = Screen(self.cols, self.rows, self.block_size)


game = Main(10, 8, 20)
time.sleep(2)
