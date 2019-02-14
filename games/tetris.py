from collections import namedtuple
import curses

point = namedtuple('Car', ['y', 'x'])

def zed(point):
    y = point.y
    x = point.x
    return [
            [y, x], [y, x+1],
            [y+1, x+1], [y+1, x+2]
            ]

def l (point):
    y = point.y
    x = point.x
    return [
            [y,x],
            [y+1, x],
            [y+2, x], [y+2, x+1] 
            ]

def box (point):
    y = point.y
    x = point.x
    return [
            [y,x],[y, x+1],
            [y+1, x], [y+1, x+1]
            ]

def draw_letter(window, points):
    for coord in points:
        window.addch(*coord, curses.ACS_CKBOARD)

def clear_letter(window, points):
    for coord in points:
        window.addch(*coord, ' ')

def tetris (stdscreen):
    curses.curs_set(0)
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, 25, 0 , width//2)
    height, width = window.getmaxyx()
    window.keypad(1)
    window.timeout(100)
    window.border(0,0,0,0,0,0,0,0)
    key = 0
    some = point(y=0, x=width//3 + 1)
    while key is not ord('q'):
        key = window.getch()
        clear_letter(window, zed(some))
        some = point(y=some.y+1, x = some.x)
        draw_letter(window, zed(some))

