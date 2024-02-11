"""Snake - v1 Establishing a PyGame screen for a snake game
by Ethan Wong"""

import pygame
import time

pygame.init()

# Initialise screen
GAME_ICON = pygame.image.load('Images/snake_icon.png')
pygame.display.set_icon(GAME_ICON)
pygame.display.set_caption("Snake game - by Ethan Wong")
SCREEN = pygame.display.set_mode((1000, 720))

# Initialise colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Import fonts
FONT1 = pygame.font.SysFont("arialblack", 20)
FONT2 = pygame.font.SysFont("consolas", 30)

# Enables game to run until user clicks 'X' at the top right of window
quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

pygame.quit()
