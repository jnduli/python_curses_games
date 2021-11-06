import curses
from collections import deque
import random

from games.errors import TerminalTooSmallError
from games.framework import Game


class Car:
    CAR_WIDTH = 3
    CAR_HEIGHT = 4

    def __init__(self, y, x, game_window):
        self.y = y
        self.x = x
        self.game_window = game_window

    def body(self):
        """Returns list with coordinates on which to draw parts of car """
        y, x = self.y, self.x
        return [[y, x+1],
                [y+1, x], [y+1, x+1], [y+1, x+2],
                [y+2, x+1],
                [y+3, x], [y+3, x+1], [y+3, x+2],
               ]

    def bounding_box(self):
        """Returns list with coordinates of the car bounding box"""
        y, x = self.y, self.x
        upper_left = [y, x]
        upper_right = [y, x+self.CAR_WIDTH]
        lower_left = [y+self.CAR_HEIGHT, x]
        lower_right = [y+self.CAR_HEIGHT, x+self.CAR_WIDTH]
        return [upper_left, upper_right, lower_left, lower_right]

    def is_point_in_car(self, point):
        # TODO: try and replace point with something else
        """Checks if point is within the car coordinates"""
        [ul, ur, ll, _] = self.bounding_box()
        [y, x] = point
        if (x >= ul[1] and x <= ur[1] and y >= ul[0] and y <= ll[0]):
            return True
        return False

    def draw(self):
        for coord in self.body():
            self.game_window.addch(*coord, curses.ACS_CKBOARD)

    def clear(self):
        for coord in self.body():
            self.game_window.addch(*coord, ' ')

    def move(self, y, x):
        """Clears car from screen then adjusts the car's coordinates"""
        self.clear()
        self.y = y
        self.x = x


def check_for_collisions(hero, villains):
    """Checks if the hero and villains have hit each other"""
    hero_points = hero.bounding_box()
    for v in villains:
        for point in hero_points:
            if v.is_point_in_car(point):
                return True
    return False


class Villains:

    def __init__(self, x_positions, game_window):
        self.villains = deque()
        self.allowed_x = x_positions
        self.game_window = game_window

    def __getitem__(self, index):
        return self.villains[index]

    def __len__(self):
        return len(self.villains)

    def random_add(self, hero, difficulty=1):
        """Randomly generates villains 70% of the time per call"""
        if not random.randint(0, 10) < 7:
            return

        villain = Car(y=0,
                      x=self.allowed_x[random.randint(0, 2)], game_window=self.game_window)

        try:
            last_villain = self.villains[-1]
            # Makes sure the generated villain and last villain don't collide
            if check_for_collisions(villain, [last_villain]):
                return
            second_last_villain = self.villains[-2]
            # Preventing three heros on a row
            # Generate villain if there is enough space for hero to manoeuvre 
            # However this prevents two heros following each other
            generate_double = random.randint(0, 10) < difficulty 
            if (generate_double
                    and last_villain.y+Car.CAR_HEIGHT >= second_last_villain.y
                    and villain.y + 9 > last_villain.y):
                return
            if (not generate_double and villain.y +9 > last_villain.y):
                return

            self.villains.append(villain)
        except IndexError:
            self.villains.append(villain)

    # TODO: control the speed of motion of villains
    def move(self):
        for v in self.villains:
            v.move(v.y+1, v.x)

    def remove(self, window):
        """Remove first car if it's beyond window height"""
        height, _ = window.getmaxyx()
        try:
            first_villain = self.villains[0]
            if (first_villain.y >= height - 4):
                self.villains.popleft().clear()
                return 1
            return 0
        except IndexError:
            return 0

    def draw(self):
        for car in self.villains:
            car.draw()


class Race(Game):
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

        self.game_window = self.create_game_window(stdscreen)
        height, width = self.game_window.getmaxyx()
        self.score_window = self.create_score_window(stdscreen)
        self.hero = Car(y=int(height*0.6), x=self.x_positions[random.randint(0, 2)], game_window=self.game_window)
        # TODO: Remove this variables
        self.left_limit = self.x_positions[0]
        self.right_limit = self.x_positions[-1]
        self.villains = Villains(self.x_positions, self.game_window)

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

    def pause(self):
        while self.game_window.getch() != ord('p'):
            continue

    def loop(self):
        key = 0
        score = 0
        level = 0
        while key is not ord('q'):
            key = self.game_window.getch()
            if key == ord('p'):
                self.pause()
            if check_for_collisions(self.hero, self.villains):
                return
            self.villains.random_add(self.hero, difficulty=level)
            self.hero.draw()
            self.villains.move()
            self.villains.draw()
            self.hero_motion(key)
            score = score + self.villains.remove(self.game_window)
            level = score // 10
            self.game_window.timeout(100 - level * 10)
            self.update_score(score=score, level=level)

    def create_game_window(self, stdscreen):
        height, width = stdscreen.getmaxyx()
        window = curses.newwin(height, self.game_width, 0, width//2)
        window.keypad(True)
        window.timeout(100)
        window.border(0, 0, 0, 0, 0, 0, 0, 0)
        return window

    def create_score_window(self, stdscreen):
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
            self.hero.move(y=self.hero.y, x=new_x)

    def update_score(self, score, level=0):
        score_message = 'Score: {}'.format(score)
        level_message = 'Level: {}'.format(level)
        height, width = self.score_window.getmaxyx()
        self.score_window.addstr(height//2 - 2, width//2, level_message)
        self.score_window.addstr(height//2, width//2, score_message)
        self.score_window.refresh()


def race_game(stdscreen):
    race = Race(stdscreen)
    race.loop()


if __name__ == '__main__':
    curses.wrapper(race_game)
