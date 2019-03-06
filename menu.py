import curses
from games.snake import snake
from games.race.__main__ import racing
from games.tetris.__main__ import tetris
from games.nogame import nogame

def menu(stdscreen):
    stdscreen.clear()
    stdscreen.keypad(True)
    curses.cbreak()
    items = {
            'Snake' : snake,
            'Racing' : racing,
            'Tetris': tetris,
            'Typing Tutor': nogame
            }
    display(stdscreen, items)

def display(stdscreen, items, menu_y=5):
    selected = 0
    stdscreen.addstr(menu_y, 1, 'Press y to start game, j/up to move up, k/down to move down, q to quit')
    menu_y = menu_y + 3
    while True:
        for index, item in enumerate(items):
            if index == selected:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL
            stdscreen.addstr(menu_y + index, 1, '{}. {}'.format(index,item), mode)
        key = stdscreen.getch()
        motion = key_motion(key)
        selected = selected + motion
        if selected < 0:
            selected = 0
        if selected >= len(items):
            selected = len(items)-1

        key_game_launcher(key, items, selected, stdscreen)
        stdscreen.refresh()

def key_motion(key):
    if key == ord('q'):
        quit()
    elif key in [curses.KEY_DOWN, ord('j')]:
        return 1
    elif key in [curses.KEY_UP, ord('k')]:
        return -1
    else:
        return 0

def key_game_launcher(key, items, index, stdscreen):
    stdscreen.addch(1, 1, key)
    if key is ord('y'):
        stdscreen.addstr(0, 1, 'In enter method')
        key = list(items)[index]
        #  nogame(stdscreen)
        items[key](stdscreen)

