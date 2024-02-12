"""Snake - v2
by Ethan Wong"""

import pygame
import time

pygame.init()

# Initialise screen
SCREEN_WIDTH, SCREEN_HEIGHT = 10, 10  # width >= 7 (snake length * 2 + 1)
BLOCK_SIZE = 20

GAME_ICON = pygame.image.load('Images/snake_icon.png')
pygame.display.set_icon(GAME_ICON)
pygame.display.set_caption("Snake game - by Ethan Wong")
SCREEN = pygame.display.set_mode((SCREEN_WIDTH*BLOCK_SIZE, SCREEN_HEIGHT*BLOCK_SIZE))

# Initialise colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Import fonts
FONT1 = pygame.font.SysFont("arialblack", 20)
FONT2 = pygame.font.SysFont("consolas", 30)

# Initialise game grid
game_grid = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

# Initialise the snake, facing left
START_X, START_Y = round(SCREEN_WIDTH/3)*2, round(SCREEN_HEIGHT/2)
player_snake = [(START_X, START_Y), (START_X + 1, START_Y), (START_X + 2, START_Y)]


def update_grid(snake):
    # reset grid
    grid = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    # add snake and apples
    for row in range(len(grid)):
        # print(f"row: {row}")
        for col in range(len(grid)):
            # print(f"col: {col}")
            for coord in snake:
                # print(f"coord[0]: {coord[0]}, coord[1]: {coord[1]}")
                if coord[0] == col and coord[1] == row:
                    grid[row][col] = 1

    for i in grid:
        print(i)
    return grid


update_grid(player_snake)


# Enables game to run until user clicks 'X' at the top right of window
quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

pygame.quit()
