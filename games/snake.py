import random
import curses

from games.framework import Game
from games.shapes import Point


class Snake:

    def __init__(self, width, height, game_window):
        snake_x = width // 4
        snake_y = height // 2
        self.game_window = game_window
        self.eaten = False
        self.direction = 'r'
        self.body = [
            Point(x=snake_x, y=snake_y),
            Point(x=snake_x - 1, y=snake_y),
            Point(x=snake_x - 2, y=snake_y),
        ]

    def is_impossible_directions(self, next_direction):
        impossible_directions = set(
                    [frozenset(['u', 'd']), frozenset(['l', 'r'])]
                )
        if frozenset([self.direction, next_direction]) in impossible_directions:
            return True
        return False

    def move(self, direction):
        new_head = Point(**self.body[0]._asdict())
        allowed_directions = set(['u', 'd', 'l', 'r'])
        if direction not in allowed_directions:
            direction = self.direction

        if self.is_impossible_directions(direction):
            direction = self.direction

        self.direction = direction
        if self.direction == 'd':
            new_head = new_head._replace(y=new_head.y + 1)
        elif self.direction == 'u':
            new_head = new_head._replace(y=new_head.y - 1)
        elif self.direction == 'l':
            new_head = new_head._replace(x=new_head.x - 1)
        elif self.direction == 'r':
            new_head = new_head._replace(x=new_head.x + 1)
        self.body.insert(0, new_head)

    def has_hit_boundary_or_itself(self, height, width):
        return (self.body[0].y in [0, height]
                or self.body[0].x in [0, width]
                or self.body[0] in self.body[1:])

    def eat_food(self, food_point):
        if self.body[0] == food_point:
            self.eaten = True
            return True
        return False

    def draw(self):
        """ Drawing the snake

        This is done by removing the tail, and just adding an extra character at the head
        """
        if not self.eaten:
            tail = self.body.pop()
            self.game_window.addch(tail.y, tail.x, ' ')
        self.game_window.addch(self.body[0].y, self.body[0].x, curses.ACS_CKBOARD)
        self.eaten = False


class Food:

    def __init__(self, width, height, disallowed_points, game_window):
        self.game_window = game_window
        while True:
            new_food = Point(x=random.randint(1, width - 1),
                             y=random.randint( 1, height - 1))
            if new_food not in disallowed_points:
                self.body = new_food
                break

    def draw(self):
        self.game_window.addch(self.body.y, self.body.x, curses.ACS_PI)


class SnakeGame(Game):
    SCOREHEIGHT = 4

    def __init__(self, stdscreen):
        curses.curs_set(0)
        self.height, self.width = stdscreen.getmaxyx()
        self.create_score_window()
        self.create_game_window()
        self.snake = Snake(self.width, self.height, self.game_window)
        self.food = Food(self.width, self.height-self.SCOREHEIGHT, self.snake.body, self.game_window)
        self.food.draw()
        self.update_score(0)

    def create_score_window(self):
        self.score_window = curses.newwin(self.SCOREHEIGHT, self.width, 0, 0)
        self.score_window.border(0, 0, 0, 0, 0, 0, 0, 0)

    def create_game_window(self):
        self.game_window = curses.newwin(self.height - self.SCOREHEIGHT,
                                         self.width, self.SCOREHEIGHT, 0)
        self.game_window.keypad(True)
        self.game_window.timeout(100)

    def update_score(self, score):
        score_message = 'Score: {}'.format(score)
        height, width = self.score_window.getmaxyx()
        self.score_window.addstr(height // 2, width // 2, score_message)
        self.score_window.refresh()

    def key_action(self, key):
        if key == ord('p'):
            self.pause()
        direction = None
        if key in [curses.KEY_DOWN, ord('j')]:
            direction = 'd'
        if key in [curses.KEY_UP, ord('k')]:
            direction = 'u'
        if key in [curses.KEY_LEFT, ord('h')]:
            direction = 'l'
        if key in [curses.KEY_RIGHT, ord('l')]:
            direction = 'r'
        self.snake.move(direction)

    def pause(self):
        while self.game_window.getch() != ord('p'):
            continue

    def loop(self):
        score = 0
        while True:
            if self.snake.has_hit_boundary_or_itself(self.height, self.width):
                return

            next_key = self.game_window.getch()
            # Quitting the game
            # TODO: move this to the key_actions method
            if next_key == ord('q'):
                break
            self.key_action(next_key)

            if self.snake.eat_food(self.food.body):
                self.food = Food(self.width, self.height-self.SCOREHEIGHT, self.snake.body, self.game_window)
                score = score + 1
                self.update_score(score)
                self.food.draw()
            self.snake.draw()


def snake_game(stdscreen):
    snake = SnakeGame(stdscreen)
    snake.loop()


if __name__ == '__main__':
    curses.wrapper(snake_game)
