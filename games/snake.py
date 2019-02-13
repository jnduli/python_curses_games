import random
import curses

def initial_snake(width, height):
    snake_x = width // 4;
    snake_y = height // 2;
    return [
            [snake_y, snake_x],
            [snake_y, snake_x-1],
            [snake_y, snake_x-2]
            ]

def initial_food(width, height):
    return [height//2, width//2]

def updateScore(scoreWindow, score):
    scoreMessage = 'Score: {}'.format(score)
    height, width = scoreWindow.getmaxyx()
    scoreWindow.addstr(height//2, width//2, scoreMessage)
    scoreWindow.refresh()

def snake(stdscreen):
    curses.curs_set(0)
    height, width = stdscreen.getmaxyx()
    scoreHeight = 4;
    scoreWindow = curses.newwin(scoreHeight, width, 0, 0)
    scoreWindow.border(0, 0, 0, 0, 0, 0, 0, 0)
    window = curses.newwin(height-scoreHeight, width, scoreHeight, 0)
    window.keypad(1)
    window.timeout(100)

    snake = initial_snake(width, height)
    food = initial_food(width, height)
    window.addch(food[0], food[1], curses.ACS_PI)
    updateScore(scoreWindow, 0)

    # Intial direction of snake
    key = curses.KEY_RIGHT
    score = 0
    while True:
        next_key = window.getch()
        key = key if next_key == -1 else next_key

        if snake[0][0] in [0, height] or snake[0][1]  in [0, width] or snake[0] in snake[1:]:
            return

        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        if snake[0] == food:
            food = None
            score = score + 1
            updateScore(scoreWindow, score)
            while food is None:
                nf = [
                    random.randint(1, height-1),
                    random.randint(1, width-1)
                ]
                food = nf if nf not in snake else None
            window.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
    return

