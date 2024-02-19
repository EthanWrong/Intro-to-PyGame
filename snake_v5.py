"""Snake - v5
by Ethan Wong"""

import pygame
import time

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

        quit_game = False
        while not quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print("left")
                    elif event.key == pygame.K_RIGHT:
                        print("right")
                    elif event.key == pygame.K_UP:
                        print("up")
                    elif event.key == pygame.K_DOWN:
                        print("down")

    def update_grid(self):
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if (c, r) == self.player.loc():  # snake head
                    self.grid[r][c] = 1
                elif (c, r) in self.player.grid:  # snake body
                    self.grid[r][c] = 2
                # elif (col_num, row_num) in apples:
                #     self.grid[row_num][col_num] = 3
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
        for r, row in enumerate(board.grid):
            for c, col in enumerate(row):
                print(col)
                colour = self.key[col]
                pygame.draw.rect(self.screen, colour, [c*self.block_size, r*self.block_size, self.block_size, self.block_size])
        pygame.display.update()








board = Board(10, 8, 20)
board.update_grid()
board.print_grid()
board.screen.show_screen(board)
