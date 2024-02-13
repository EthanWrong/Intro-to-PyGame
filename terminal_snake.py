"""Snake game with as many apples as you want (a specified number)
Copied from code I made Aug 22, 2023, intended for the terminal:
 https://github.com/EthanWrong/terminal_apps/blob/main/snake.py

How to run:
1) Install curses: pip install windows-curses
2) Open Terminal: Win + R, cmd, Enter
3) Navigate to the folder: cd "<path to folder>"
4) Run the file: python terminal_snake.py
"""
import curses
import time
import math
import random


def generate_grid(x, y):
    grid = []
    for line in range(y):
        grid.append([])
        for col in range(x):
            grid[line].append(0)

    return grid


def update_grid(screen, player, apples):
    for row_num, row in enumerate(screen["grid"]):
        for col_num, col in enumerate(row):
            if [row_num, col_num] == player["grid"][0]:  # snake head
                screen["grid"][row_num][col_num] = 2
            elif [row_num, col_num] in player["grid"]:  # snake body
                screen["grid"][row_num][col_num] = 1
            elif [row_num, col_num] in apples:
                screen["grid"][row_num][col_num] = "APPLE"
            else:
                screen["grid"][row_num][col_num] = 0
    return screen


def show_screen(screen, win, key, pixel_width, pixel_height, msg):
    TOP_PAD = 1 if pixel_height > 1 else 0
    LEFT_PAD = pixel_height
    msg = f"{LEFT_PAD*' '}{msg}"

    for row_num, row in enumerate(screen["grid"]):

        for pixel in range(pixel_height):
            X = 0
            win.move((row_num * pixel_height) + pixel, X)

            for col_num, col in enumerate(row):
                CHAR = key[col][0] * pixel_width
                ATTR = key[col][1]

                if pixel == TOP_PAD and msg:
                    CHAR = msg[0:pixel_width].ljust(pixel_width)
                    msg = msg[pixel_width:]

                if row_num == screen["rows"] - 1 and col_num == screen["cols"] - 1:
                    # prevents cursor from moving off-screen when addstr to bottom right corner
                    win.insstr(CHAR, ATTR)
                else:
                    win.addstr(CHAR, ATTR)

    return screen


def generate_colors():
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    GREEN = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    BLACK = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    RED = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
    BLUE = curses.color_pair(4)

    return GREEN, BLACK, RED, BLUE


def process_keypress(char):
    if char == 260:
        return "left"
    elif char == 261:
        return "right"
    elif char == 259:
        return "up"
    elif char == 258:
        return "down"
    elif char == ord("q"):
        return "quit"
    elif char == 32:
        return "Space"
    else:
        return None


def change_player_direction(new_dir, current_dir):
    if new_dir == "left" and current_dir == "right" or new_dir == "right" and current_dir == "left" or \
            new_dir == "up" and current_dir == "down" or new_dir == "down" and current_dir == "up":
        return current_dir
    else:
        return new_dir


def update_player(player, screen, grow=False):
    PLAYER_ROW = player["grid"][0][0]
    PLAYER_COL = player["grid"][0][1]
    RIGHT = [PLAYER_ROW, PLAYER_COL + 1]
    LEFT = [PLAYER_ROW, PLAYER_COL - 1]
    UP = [PLAYER_ROW - 1, PLAYER_COL]
    DOWN = [PLAYER_ROW + 1, PLAYER_COL]

    if player["dir"] == "right":
        if PLAYER_COL == screen["cols"]-1:  # hits wall
            player["alive"] = False
        elif screen["grid"][PLAYER_ROW][PLAYER_COL+1] == 1:  # hits self
            player["alive"] = False
        else:
            player["grid"].insert(0, RIGHT)
    elif player["dir"] == "left":
        if PLAYER_COL == 0:  # hits wall
            player["alive"] = False
        elif screen["grid"][PLAYER_ROW][PLAYER_COL-1] == 1:  # hits self
            player["alive"] = False
        else:
            player["grid"].insert(0, LEFT)
    elif player["dir"] == "up":
        if PLAYER_ROW == 0:  # hits wall
            player["alive"] = False
        elif screen["grid"][PLAYER_ROW-1][PLAYER_COL] == 1:
            player["alive"] = False
        else:
            player["grid"].insert(0, UP)
    elif player["dir"] == "down":
        if PLAYER_ROW == screen["rows"] - 1:
            player["alive"] = False
        elif screen["grid"][PLAYER_ROW+1][PLAYER_COL] == 1:
            player["alive"] = False
        else:
            player["grid"].insert(0, DOWN)

    if not grow:
        player["grid"].pop()
    else:
        player["score"] += 1

    return player


def generate_apple(screen, player):
    while True:
        loc = [random.randint(0, screen["rows"] - 1), random.randint(0, screen["cols"] - 1)]
        if loc not in player["grid"]:
            return loc


def start_menu(win):
    while True:
        char = win.getch()
        if process_keypress(char) == "right":
            return


def main(stdscr, highscore=0):
    # generate colors
    GREEN, BLACK, RED, BLUE = generate_colors()

    stdscr.nodelay(True)
    curses.curs_set(0)

    PIXEL_WIDTH = 4
    PIXEL_HEIGHT = 2

    TICK_SPEED = 0.1

    KEY = {  # Character - Attribute pairs
        0: (" ", GREEN),
        1: (" ", BLACK),
        "APPLE": (" ", RED),
        2: (" ", BLUE)
    }

    # set up screen
    WIN_ROWS, WIN_COLS = stdscr.getmaxyx()
    ROWS = int(WIN_ROWS / PIXEL_HEIGHT) if WIN_ROWS % PIXEL_HEIGHT == 0 else int(math.floor(WIN_ROWS / PIXEL_HEIGHT))
    COLS = int(WIN_COLS / PIXEL_WIDTH) if WIN_COLS % PIXEL_WIDTH == 0 else int(math.floor(WIN_COLS / PIXEL_WIDTH))

    NUM_APPLES = 10

    screen = {
        "rows": ROWS,
        "cols": COLS,
        "grid": generate_grid(COLS, ROWS)
    }

    # initialise player
    player = {
        "grid": [  # y, x
            [1, 3],
            [1, 2],
            [1, 1]
        ],
        "score": 0,
        "dir": "right",
        "alive": True,
        "highscore": highscore
    }
    apples = [generate_apple(screen, player) for i in range(NUM_APPLES)]

    screen = update_grid(screen, player, apples)

    show_screen(screen, stdscr, KEY, PIXEL_WIDTH, PIXEL_HEIGHT, "Press Right Arrow to Start")

    start_menu(stdscr)

    START_TIME = time.time()

    while player["alive"]:
        current_time = round(time.time() - START_TIME, 1)

        char = stdscr.getch()
        key = process_keypress(char)
        if not key:
            pass
        elif key == "quit":
            break
        else:  # direction key
            player["dir"] = change_player_direction(key, player["dir"])

        if player["grid"][0] in apples:
            grow = True
            # apples.append(generate_apple(screen, player))
            apples[apples.index(player["grid"][0])] = generate_apple(screen, player)
        else:
            grow = False

        player = update_player(player, screen, grow)

        screen = update_grid(screen, player, apples)

        msg = f"Score: {player['score']}   |   Highscore: {player['highscore']}   |   Time: {current_time}"
        show_screen(screen, stdscr, KEY, PIXEL_WIDTH, PIXEL_HEIGHT, msg)

        time.sleep(TICK_SPEED)

    time.sleep(3)
    player["highscore"] = player["score"] if player["score"] > player["highscore"] else player["highscore"]
    main(stdscr, player["highscore"])


if __name__ == "__main__":
    curses.wrapper(main)
