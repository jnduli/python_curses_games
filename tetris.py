import curses

MOTION = 3
def car(window, y, x):
    window.addch(y, x+1, curses.ACS_CKBOARD) 
    window.addch(y+1, x, curses.ACS_CKBOARD)
    window.addch(y+1, x+1, curses.ACS_CKBOARD)
    window.addch(y+1, x+2, curses.ACS_CKBOARD)
    window.addch(y+2, x+1, curses.ACS_CKBOARD)
    window.addch(y+3, x, curses.ACS_CKBOARD)
    window.addch(y+3, x+1, curses.ACS_CKBOARD)
    window.addch(y+3, x+2, curses.ACS_CKBOARD)

def tetris(stdscreen):
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, 13, 0 , width//2 - 2)
    height, width = window.getmaxyx()
    window.keypad(1)
    #  window.timeout(100)
    window.border(0,0,0,0,0,0,0,0)
    key = 0
    hero = [height//2, width//3]
    left_limit = 0
    right_limit = 6
    while key is not ord('q'):
        key = window.getch()
        car(window, *hero)
        new_x = hero_motion(key) * 3 + hero[1]
        if new_x < left_limit:
            new_x = left_limit
        if new_x > right_limit:
            new_x = right_limit
        hero[1] = new_x
        window.refresh()
        #  car(window, height//2, width//2)

def hero_motion(key):
    if key in [curses.KEY_LEFT, ord('h')]:
        return 1
    elif key in [curses.KEY_RIGHT, ord('l')]:
        return -1
    else:
        return 0
