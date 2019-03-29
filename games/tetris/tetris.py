import curses
import random
import time
from .shapes import shapes
import logging


def get_random_shape(y, x):
    return shapes[random.randint(0, len(shapes)-1)](y=y, x=x)


class ScreenBlocks:

    def __init__(self, width, height, padding):
        self.shape = [[0 for i in range(0, width+1)] for i in range(0, height)]
        self.padding = padding
        self.leftlimit = padding
        self.rightlimit = width - padding
        self.score = 0

    def is_occupied(self, y, x):
        return self.shape[y][x] == 1

    def check_shape_touched_floor(self, shape):
        for coord in shape:
            if (int(coord.y) == len(self.shape)-1):
                return True
            if self.is_occupied(int(coord.y)+1, int(coord.x)):
                return True
        return False

    def occupy(self, shape):
        for coord in shape:
            self.shape[int(coord.y)][int(coord.x)] = 1

    def draw(self, window):
        for y, row in enumerate(self.shape):
            for x, point in enumerate(row):
                if point == 1:
                    window.addch(y, x, curses.ACS_CKBOARD)
                elif x > self.padding and x < len(self.shape[0])-self.padding-2:
                    window.addch(y, x, ' ')

    def clear_and_score(self):
        logging.info('Last 2')
        logging.info(self.shape[-2])
        logging.info(self.shape[-1])
        for row in self.shape:
            if 0 not in row[self.padding:-self.padding]:
                logging.info('Removing row')
                logging.info(self.shape)
                # Remove the whole row
                self.shape.remove(row)
                # Append black row to top
                self.shape.insert(0, [0 for i in range(0, len(row))])
                score = score + 1
        return score


class Tetris:
    SCREEN_WIDTH = 15
    DOWNWARDS_SPEED = 0.01  # number of characters to move down per second
    PADDING = 1

    def __init__(self, stdscreen):
        curses.curs_set(0)
        height, width = stdscreen.getmaxyx()
        # TODO: Add error checking for width and height
        self.create_game_board(height, width)
        self.screen_blocks = ScreenBlocks(self.SCREEN_WIDTH-self.PADDING, height-self.PADDING, self)

    def create_game_board(self, height, width):
        self.window = curses.newwin(height, self.SCREEN_WIDTH, 0, width//2)
        self.window.keypad(1)
        self.window.timeout(41)  # This is set to throttle cpu usage
        self.window.border(0, 0, 0, 0, 0, 0, 0, 0)

    def loop(self):
        prev_time = time.time_ns()

        height, width = self.window.getmaxyx()
        key = 0
        shape = None
        while key is not ord('q'):
            if (shape is None):
                shape = get_random_shape(y=0, x=width//3 + 1)
            self.key_motion(key, shape, self.screen_blocks.rightlimit, self.screen_blocks.leftlimit)
            if (should_move(prev_time)):
                shape.move_down(self.window)
                prev_time = time.time_ns()

            if self.screen_blocks.check_shape_touched_floor(shape.shape):
                self.screen_blocks.occupy(shape.shape)
                shape = None
            self.screen_blocks.clear_and_score()
            self.screen_blocks.draw(self.window)
            if shape:
                shape.draw(self.window)
            key = self.window.getch()

    def key_motion(self, key, shape, rightlimit, leftlimit=0):
        if key is ord('r'):
            shape.rotate_clockwise(self.window, rightlimit, leftlimit)
        elif key in [curses.KEY_LEFT, ord('h')]:
            shape.move_left(leftlimit, self.window)
        elif key in [curses.KEY_RIGHT, ord('l')]:
            shape.move_right(rightlimit, self.window)
        elif key in [curses.KEY_DOWN, ord('j')]:
            shape.move_down(self.window)


def should_move(prevtime, downwards_speed=Tetris.DOWNWARDS_SPEED):
    nanos = 1000000 / downwards_speed
    if (time.time_ns() - prevtime) >= nanos:
        return True
    return False
