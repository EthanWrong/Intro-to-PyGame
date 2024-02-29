"""Snake - created as an intro to pygame.

Instructions:
- press Space to pause game
- press 'Q' to quit the game
- arrow keys to move

Notes:
    A very messy version of snake. The code is like spaghetti--it started off
    organised in classes, but I did not put enough forethought into the
    program and ended up having to patchwork-code towards the end.
    Game works, so I'm happy.

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
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.player = Player(self.load_highscore())

        self.screen = Screen(self.cols, self.rows, self.block_size)

        # Initialise apples
        self.NUM_APPLES = 3
        self.apples = [self.get_rand_coords() for _ in range(self.NUM_APPLES)]

        self.speed = 8
        self.clock = pygame.time.Clock()

        # Create a variable to track game state
        self.pause = False

        # Run the game; main game loop
        while True:
            self.reset_game()
            replay = self.main()
            if not replay:
                return

    @staticmethod
    def wait_to_start():
        # wait for user to press key before starting
        while True:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        return True

    def reset_game(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.player = Player(self.player.highscore)
        self.apples = [self.get_rand_coords() for _ in range(self.NUM_APPLES)]

    def main(self):
        # display screen
        self.update_grid()
        self.screen.show_screen(self, player=self.player, start_screen=True)

        # wait for user to start
        if not self.wait_to_start():
            return False  # quit pygame

        while True:

            # exit game loop if dead
            if not self.player.alive:
                break

            # display screen
            if not self.pause:
                self.update_grid()
                self.screen.show_screen(self, player=self.player)

                self.clock.tick(self.speed)
                # time.sleep(1/self.speed)

            # main game loop
            direction_changed = False  # reset flag at start of each tick
            for event in pygame.event.get():

                if event.type == pygame.QUIT:  # quit
                    return False

                if event.type == pygame.KEYDOWN:
                    self.pause = False

                    if event.key == pygame.K_q:  # quit
                        return False

                    if event.key == pygame.K_SPACE:  # pause
                        self.pause = True
                        pygame.event.clear()

                    if not direction_changed:  # check if a direction change
                        # has already been made
                        if event.key in (pygame.K_LEFT, pygame.K_RIGHT,
                                         pygame.K_UP, pygame.K_DOWN):
                            self.player.change_direction(event.key)
                            direction_changed = True  # set the flag to true
                            # after changing direction

            if self.player.loc() in self.apples:  # player is eating an apple
                grow = True
                self.apples[
                    self.apples.index(self.player.loc())] = (
                    self.get_rand_coords())  # replaces apple with new
            else:
                grow = False

            if not self.pause:  # game is un-paused
                # update player
                self.player.update(self.cols, self.rows, grow)

            if self.pause:  # game is paused
                self.screen.show_screen(self, self.player, pause=True)

        # show death screen
        self.screen.show_screen(self, player=self.player, death_screen=True)
        if self.player.highscore > self.load_highscore():
            self.save_highscore()
        time.sleep(0.5)  # give a pause to ensure no more input is taken
        pygame.event.clear()
        while True:
            event = pygame.event.wait(1000000000)  # wait for user input for an
            # arbitrarily large time
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
            return True

    def get_rand_coords(self):
        while True:
            coords = (random.randint(0, self.cols - 1),
                      random.randint(0, self.rows - 1))
            if coords not in self.player.grid:
                return coords

    def update_grid(self):
        for r, row in enumerate(self.grid):
            for c, col in enumerate(row):
                if (c, r) == self.player.loc():  # snake head
                    self.grid[r][c] = "head"
                elif (c, r) in self.player.grid:  # snake body
                    self.grid[r][c] = "body"
                elif (c, r) in self.apples:
                    self.grid[r][c] = "apple"
                else:
                    self.grid[r][c] = "grass"

    def print_grid(self):
        for row in self.grid:
            print(row)

    @staticmethod
    def load_highscore():
        try:
            highscore_file = open("highscore.txt", "r")
        except IOError:
            highscore_file = open("highscore.txt", "w")
            highscore_file.write("0")
        highscore_file = open("highscore.txt", "r")
        value = highscore_file.read()
        highscore_file.close()
        return int(value)

    def save_highscore(self):
        highscore_file = open("highscore.txt", "w")
        highscore_file.write(str(self.player.highscore))
        highscore_file.close()


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
        # changes the direction of the player, as long as the player isn't
        # already moving in the opposite direction
        if key == pygame.K_LEFT and self.direction != "right":
            self.direction = "left"
        elif key == pygame.K_RIGHT and self.direction != "left":
            self.direction = "right"
        elif key == pygame.K_UP and self.direction != "down":
            self.direction = "up"
        elif key == pygame.K_DOWN and self.direction != "up":
            self.direction = "down"

    def update(self, cols, rows, grow=False, move=True):
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
            if right[0] >= cols or right in self.grid:
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
            if down[1] >= rows or down in self.grid:
                self.alive = False
                return
            else:
                self.grid.insert(0, down)

        if not grow:
            # deletes end of snake list
            self.grid.pop()
        else:
            self.score += 1
            if self.score > self.highscore:
                self.highscore = self.score


# Class to handle the game's rendering
class Screen:
    def __init__(self, width, height, block_size):
        self.block_size = block_size

        self.width = width * self.block_size
        self.height = height * self.block_size

        # Initialise screen
        self.GAME_ICON = pygame.image.load('Images/snake_icon.png')
        pygame.display.set_icon(self.GAME_ICON)
        pygame.display.set_caption("Snake game - by Ethan Wong")
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Initialise colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.LIGHTGREEN = (0, 230, 0)
        self.GREEN = (0, 204, 0)
        self.BLUE = (0, 102, 204)
        self.DARKBLUE = (0, 77, 153)
        self.GREY = (150, 150, 150)
        self.LIGHTLIGHTBLUE = (179, 218, 255)
        self.LIGHTBLUE = (102, 179, 255)

        self.GRASS1 = self.LIGHTGREEN
        self.GRASS2 = self.GREEN

        # Import fonts
        self.FONT1 = pygame.font.SysFont("consolas", 20)
        self.FONT2 = pygame.font.SysFont("consolas", 30)

        # Initialise key
        self.key = {
            "grass": (self.GRASS1, self.GRASS2),
            "body": self.BLUE,
            "head": self.DARKBLUE,
            "apple": self.RED,
            "death_head": self.BLACK,
            "death_body": self.BLACK
        }

    def message(self, msg, font, txt_colour, center):
        txt = font.render(msg, True, txt_colour)

        text_box = txt.get_rect(center=center)
        self.screen.blit(txt, text_box)

    def show_screen(self, board, player, death_screen=False,
                    start_screen=False, pause=False):

        lighter_shade_of_grass = True  # toggleable variable to create
        # checkerboard background

        # renders the screen
        for r, row in enumerate(board.grid):
            lighter_shade_of_grass ^= True  # toggles variable
            for c, col in enumerate(row):

                x, y = c * self.block_size, r * self.block_size

                # first draw the checkerboard background
                lighter_shade_of_grass ^= True  # toggles variable
                colour = self.key["grass"][0] if lighter_shade_of_grass else\
                    self.key["grass"][1]  # creates checkerboard
                pygame.draw.rect(self.screen, colour,
                                 [x, y, self.block_size, self.block_size])

                # then add the snake or apple
                if col in ("body", "head"):  # snake head and body
                    colour = self.key[col]

                    if death_screen and col == "head":
                        colour = self.key["death_head"]
                    if death_screen and col == "body":
                        colour = self.key["death_body"]

                    pygame.draw.rect(self.screen, colour,
                                     [x, y,
                                      self.block_size, self.block_size])
                elif col == "apple":  # apple
                    apple_img = pygame.image.load(
                        "Images/minecraft_apple.png").convert_alpha()
                    apple_size = self.block_size - 1
                    apple_sprite = pygame.transform.smoothscale(apple_img,
                                                                [apple_size,
                                                                 apple_size])
                    self.screen.blit(apple_sprite, [x, y])

        # show messages
        self.message(f"{player.score}", self.FONT2, self.WHITE,
                     center=(self.block_size * 1.5, self.block_size * 1.5))
        self.message(f"{player.highscore}", self.FONT2, self.WHITE,
                     center=(self.width - self.block_size * 1.5,
                             self.block_size * 1.5))

        if death_screen:
            self.message("Game Over", self.FONT2, self.WHITE,
                         center=(self.width / 2, self.height / 2 - 40))
            self.message("Press 'q' to quit, and any other key to play again",
                         self.FONT1, self.WHITE,
                         center=(self.width / 2, self.height / 2))

        if start_screen:
            self.message("Press Right Arrow to start", self.FONT1, self.WHITE,
                         center=(self.width / 2, self.height / 4))

        if pause:
            self.message("Paused", self.FONT2, self.WHITE,
                         center=(self.width / 2, self.height / 2 - 40))
            self.message("Press any key to continue", self.FONT1, self.WHITE,
                         center=(self.width / 2, self.height / 2))

        pygame.display.update()


snake_game = Board(20, 20, 30)
pygame.quit()
