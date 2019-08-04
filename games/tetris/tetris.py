import curses
import random
import time
from .shapes import shapes
from games.errors import TerminalTooSmallError
import copy


def get_random_shape(y, x):
    return shapes[random.randint(0, len(shapes)-1)](y=y, x=x)


class ActiveGameArea:

    def __init__(self, height, width):
        self.board = [[' ' for i in range(width+1)] for j in range(height+1)]
        self.width = width
        self.height = height

    def matrix(self, shape=None):
        if shape is None:
            return self.board
        temp_board = copy.deepcopy(self.board)
        if shape is not None:
            for point in shape.shape:
                temp_board[int(point.y)][int(point.x)] = curses.ACS_CKBOARD
        return temp_board

    def check_shape_touched_floor(self, shape):
        try:
            for coord in shape.shape:
                if self.board[int(coord.y)+1][int(coord.x)] != ' ':
                    return True
        except IndexError:
            return True
        return False

    def occupy(self, shape):
        for coord in shape:
            self.board[int(coord.y)][int(coord.x)] = curses.ACS_CKBOARD

    def clear(self):
        score = 0
        for row in self.board:
            if ' ' not in row:
                self.board.insert(0, [' ' for i in range(len(row))])
                self.board.remove(row)
                score = score + 1
        return score


class Tetris:
    SCREEN_WIDTH = 15
    MIN_HEIGHT = 20
    INFO_WIDTH = 10
    PADDING = 2

    def __init__(self, stdscreen):
        curses.curs_set(0)
        height, width = stdscreen.getmaxyx()
        if height < self.MIN_HEIGHT:
            raise TerminalTooSmallError("The terminal height is too small")
        if width < self.SCREEN_WIDTH + self.INFO_WIDTH:
            raise TerminalTooSmallError("The terminal widht is too small")
        if time.get_clock_info('time').resolution > 1e-03:
            raise Exception('Clock too slow for use')

        self.create_game_board(height, width)
        self.create_game_board(height, width)
        active_h, active_w = self.window.getmaxyx()
        self.active_board = ActiveGameArea(
                active_h-(self.PADDING*2),
                active_w-(self.PADDING*2))
        self.rightlimit = active_w - (self.PADDING*2)
        self.create_info_board()

    def create_game_board(self, height, width):
        self.score = 0
        self.window = curses.newwin(height, self.SCREEN_WIDTH, 0, width//2)
        self.window.keypad(1)
        self.window.timeout(141)  # This is set to throttle cpu usage
        self.window.border(0, 0, 0, 0, 0, 0, 0, 0)

    def create_info_board(self):
        # Should be called after create_game_board
        (_, x) = self.window.getbegyx()
        (height, win_width) = self.window.getmaxyx()
        game_right_x = x + win_width
        self.info_window = curses.newwin(
                height, self.INFO_WIDTH, 0, game_right_x + self.PADDING * 2)
        self.info_window.border(0, 0, 0, 0, 0, 0, 0, 0)
        self.info_window.refresh()

    def render(self, matrix):
        for y, row in enumerate(matrix):
            for x, char in enumerate(row):
                self.window.addch(y+self.PADDING, x+self.PADDING, matrix[y][x])

    def loop(self):
        key = 0
        shape = None
        while key is not ord('q'):
            key = self.window.getch()
            if shape is None:
                active_h, active_w = self.window.getmaxyx()
                shape = get_random_shape(y=self.PADDING, x=(active_w-1)//3)
            if self.active_board.check_shape_touched_floor(shape):
                self.active_board.occupy(shape)
                score = self.active_board.clear()
                if score > 0:
                    self.score += score
                    self.update_info()
                shape = None
            else:
                self.key_motion(key, shape, self.rightlimit)
                shape.move_down()
            matrix = self.active_board.matrix(shape)
            self.render(matrix)

    def key_motion(self, key, shape, rightlimit, leftlimit=0):
        #  if key is ord('p'):
        #  self.pause = not self.pause
        if key is ord('r'):
            shape.rotate_clockwise(rightlimit, leftlimit)
        elif key in [curses.KEY_LEFT, ord('h')]:
            shape.move_left(leftlimit)
        elif key in [curses.KEY_RIGHT, ord('l')]:
            shape.move_right(rightlimit)
        #  elif key in [curses.KEY_DOWN, ord('j')]:
            #  shape.move_down()

    def update_info(self):
        message = 'Score:'
        self.info_window.addstr(10, 2, message)
        self.info_window.addstr(11, 2, str(self.score))
        self.info_window.refresh()
