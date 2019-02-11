import curses

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
    window = curses.newwin(height, width, 0, 0)
    window.keypad(1)
    window.timeout(100)
    key = 0
    while key is not ord('q'):
        key = window.getch()
        car(window, height//2, width//2)

