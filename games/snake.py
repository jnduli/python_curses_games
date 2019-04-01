import random
import curses


def initial_snake(width, height):
    snake_x = width // 4
    snake_y = height // 2
    return [
            [snake_y, snake_x],
            [snake_y, snake_x-1],
            [snake_y, snake_x-2]
            ]


def initial_food(width, height):
    return [height//2, width//2]


class Snake:
    SCOREHEIGHT = 4

    def __init__(self, stdscreen):
        curses.curs_set(0)
        self.height, self.width = stdscreen.getmaxyx()
        self.create_score_window()
        self.create_game_window()
        self.snake = initial_snake(self.width, self.height)
        self.food = initial_food(self.width, self.height)
        self.game_window.addch(self.food[0], self.food[1], curses.ACS_PI)
        self.update_score(0)

    def create_score_window(self):
        self.score_window = curses.newwin(self.SCOREHEIGHT, self.width, 0, 0)
        self.score_window.border(0, 0, 0, 0, 0, 0, 0, 0)

    def create_game_window(self):
        self.game_window = curses.newwin(
                self.height-self.SCOREHEIGHT, self.width, self.SCOREHEIGHT, 0)
        self.game_window.keypad(1)
        self.game_window.timeout(100)

    def update_score(self, score):
        scoreMessage = 'Score: {}'.format(score)
        height, width = self.score_window.getmaxyx()
        self.score_window.addstr(height//2, width//2, scoreMessage)
        self.score_window.refresh()

    def snake_beyond_boundaries_or_hit_itself(self):
        return (self.snake[0][0] in [0, self.height]
                or self.snake[0][1] in [0, self.width]
                or self.snake[0] in self.snake[1:])

    def move_snake(self, key):
        new_head = [self.snake[0][0], self.snake[0][1]]
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        self.snake.insert(0, new_head)

    def new_food(self):
        while True:
            new_food = [
                random.randint(1, self.height - self.SCOREHEIGHT - 1),
                random.randint(1, self.width-1)
            ]
            if new_food not in self.snake:
                return new_food

    def eat_food(self):
        if self.snake[0] == self.food:
            self.food = self.new_food()
            return True
        return False

    def loop(self):
        # Initial direction of snake
        key = curses.KEY_RIGHT
        score = 0
        while True:
            next_key = self.game_window.getch()
            key = key if next_key == -1 else next_key

            if self.snake_beyond_boundaries_or_hit_itself():
                return
            self.move_snake(key)
            if self.eat_food():
                score = score + 1
                self.update_score(score)
                self.game_window.addch(self.food[0], self.food[1], curses.ACS_PI)
            else:
                tail = self.snake.pop()
                self.game_window.addch(tail[0], tail[1], ' ')
            self.game_window.addch(self.snake[0][0], self.snake[0][1], curses.ACS_CKBOARD)


def snake_game(stdscreen):
    snake = Snake(stdscreen)
    snake.loop()

if __name__ == '__main__':
    curses.wrapper(snake_game)
