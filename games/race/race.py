import curses
from random import randint
from .car import Car
from .villains import Villains
from .collisions import Collision
from games.errors import TerminalTooSmallError


class Race(Collision):
    MIN_HEIGHT = 20
    MIN_WIDTH = 40
    PADDING = 1

    def __init__(self, stdscreen):
        curses.curs_set(0)
        screen_height, screen_width = stdscreen.getmaxyx()

        if screen_height < Race.MIN_HEIGHT:
            raise TerminalTooSmallError('The screen height is too small')
        if screen_width < Race.MIN_WIDTH:
            raise TerminalTooSmallError('The width is too small')

        self.game_window = self.create_game_board(stdscreen)
        height, width = self.game_window.getmaxyx()
        self.score_window = self.create_score_board(stdscreen)
        self.hero = Car(y=int(height*0.6), x=self.x_positions[randint(0, 2)])
        # TODO: Remove this variables
        self.left_limit = self.x_positions[0]
        self.right_limit = self.x_positions[-1]
        self.villains = Villains(self.x_positions)

    @property
    def x_positions(self):
        """ Returns a list containing possible positions of the cars """
        first = self.PADDING 
        second = first + Car.CAR_WIDTH + self.PADDING
        third = second + Car.CAR_WIDTH + self.PADDING
        return [first, second, third]

    @property
    def game_width(self):
        return self.x_positions[-1] + Car.CAR_WIDTH + self.PADDING

    def loop(self):
        key = 0
        score = 0
        level = 0
        while key is not ord('q'):
            key = self.game_window.getch()
            if (self.check_for_collisions(self.hero, self.villains)):
                return
            self.villains.random_add(self.hero, difficulty=level)
            self.hero.draw(self.game_window)
            self.villains.move(self.game_window)
            self.villains.draw(self.game_window)
            self.hero_motion(key)
            score = score + self.villains.remove(self.game_window)
            level = score // 10
            self.game_window.timeout(100 - level * 10)
            self.update_score(score=score, level=level)

    def create_game_board(self, stdscreen):
        height, width = stdscreen.getmaxyx()
        window = curses.newwin(height, self.game_width, 0, width//2)
        window.keypad(1)
        window.timeout(100)
        window.border(0, 0, 0, 0, 0, 0, 0, 0)
        return window

    def create_score_board(self, stdscreen):
        height, width = stdscreen.getmaxyx()
        quit_message = 'Press q to quit'
        score_width = len(quit_message) + self.PADDING * 2
        window = curses.newwin(height, score_width, 0, width//2 + self.game_width)
        window.border(0, 0, 0, 0, 0, 0, 0, 0)
        window.addstr(height//2 - 5, 1, quit_message)
        window.refresh()
        return window

    def hero_motion(self, key):
        new_x = self.hero.x
        motion_distance = self.hero.CAR_WIDTH + self.PADDING
        if key in [curses.KEY_LEFT, ord('h')]:
            new_x = -motion_distance + new_x
        elif key in [curses.KEY_RIGHT, ord('l')]:
            new_x = motion_distance + new_x

        left_limit = self.x_positions[0]
        right_limit = self.x_positions[-1]
        if new_x < left_limit:
            new_x = left_limit
        if new_x > right_limit:
            new_x = right_limit
        if self.hero.x is not new_x:
            self.hero.move(self.game_window, y=self.hero.y, x=new_x)

    def update_score(self, score, level=0):
        score_message = 'Score: {}'.format(score)
        level_message = 'Level: {}'.format(level)
        height, width = self.score_window.getmaxyx()
        self.score_window.addstr(height//2 - 2, width//2, level_message)
        self.score_window.addstr(height//2, width//2, score_message)
        self.score_window.refresh()
