"""Snake - v9
Added collision detecting and dying

To add:
- proper death screen
- nicer movement / input

by Ethan Wong"""

import pygame
import time
import random

pygame.init()


# Class to handle the game's logic
class Board:
    def __init__(self, cols, rows, block_size):
        self.cols = cols
        self.rows = rows
        self.block_size = block_size

        # Initialise grid, in which the game logic will be done
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.player = Player(0)

        self.screen = Screen(self.cols, self.rows, self.block_size)

        # Initialise apples
        self.NUM_APPLES = 3
        self.apples = [self.get_rand_coords() for _ in range(self.NUM_APPLES)]

        # Run the game; main game loop
        clock = pygame.time.Clock()
        quit_game = False
        while not quit_game:

            if not self.player.alive:
                break

            direction_changed = False  # reset flag at start of each tick
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit_game = True

                    if not direction_changed:  # check if a direction change has already been made
                        if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                            self.player.change_direction(event.key)
                            direction_changed = True  # set the flag to true after changing direction

            if self.player.loc() in self.apples:  # player is eating an apple
                grow = True
                self.apples[self.apples.index(self.player.loc())] = self.get_rand_coords()  # replaces apple with new
            else:
                grow = False

            self.player.update(self.cols, self.rows, grow)
            self.update_grid()
            self.screen.show_screen(self)

            clock.tick(8)

    def get_rand_coords(self):
        while True:
            coords = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            if coords not in self.player.grid:
                return coords

    def update_grid(self):
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if (c, r) == self.player.loc():  # snake head
                    self.grid[r][c] = 1
                elif (c, r) in self.player.grid:  # snake body
                    self.grid[r][c] = 2
                elif (c, r) in self.apples:
                    self.grid[r][c] = 3
                else:
                    self.grid[r][c] = 0

    def print_grid(self):
        for row in self.grid:
            print(row)


class Player:
    def __init__(self, highscore=0):
        self.grid = [  # x, y
            (3, 1),
            (2, 1),
            (1, 1)
        ]
        self.score = 0
        self.direction = "right"
        self.alive = True
        self.highscore = highscore

    def col(self):
        return self.grid[0][0]

    def row(self):
        return self.grid[0][1]

    def loc(self):
        return self.grid[0][0], self.grid[0][1]

    def change_direction(self, key):
        # changes the direction of the player, as long as the player isn't already moving in the opposite direction
        if key == pygame.K_LEFT and self.direction != "right":
            self.direction = "left"
        elif key == pygame.K_RIGHT and self.direction != "left":
            self.direction = "right"
        elif key == pygame.K_UP and self.direction != "down":
            self.direction = "up"
        elif key == pygame.K_DOWN and self.direction != "up":
            self.direction = "down"

    def update(self, cols, rows, grow=False):
        # coords to add to snake list
        left = (self.col() - 1, self.row())
        right = (self.col() + 1, self.row())
        up = (self.col(), self.row() - 1)
        down = self.col(), self.row() + 1

        # adds coords to start of snake list
        if self.direction == "left":
            if left[0] < 0 or left in self.grid:
                self.alive = False
                return
            else:
                self.grid.insert(0, left)
        elif self.direction == "right":
            if right[0] > cols or right in self.grid:
                self.alive = False
                return
            else:
                self.grid.insert(0, right)
        elif self.direction == "up":
            if up[1] < 0 or up in self.grid:
                self.alive = False
                return
            else:
                self.grid.insert(0, up)
        elif self.direction == "down":
            if down[1] > rows or down in self.grid:
                self.alive = False
                return
            else:
                self.grid.insert(0, down)

        if not grow:
            # deletes end of snake list
            self.grid.pop()
        else:
            self.score += 1
            print(self.score)


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
        self.screen = pygame.display.set_mode((width * block_size, height * block_size))

        # Initialise colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Import fonts
        self.FONT1 = pygame.font.SysFont("arialblack", 20)
        self.FONT2 = pygame.font.SysFont("consolas", 30)

        # Initialise key
        self.key = {
            0: self.GREEN,
            2: self.BLACK,
            1: self.BLUE,
            3: self.RED,
        }

    def show_screen(self, board):
        # renders the screen
        for r, row in enumerate(board.grid):
            for c, col in enumerate(row):
                colour = self.key[col]
                pygame.draw.rect(self.screen, colour,
                                 [c * self.block_size, r * self.block_size, self.block_size, self.block_size])
        pygame.display.update()


snake_game = Board(20, 20, 30)
