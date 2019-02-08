import curses

def menu(stdscreen):
    stdscreen.clear()
    items = ['Snake', 'Tetris(Not implemented)', 'Typing Tutor(Not Implemented)']
    display(stdscreen, items)

def display(stdscreen, items, menu_y=5):
    selected = 0
    while True:
        for index, item in enumerate(items):
            if index == selected:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL
            stdscreen.addstr(menu_y + index, 1, '{}. {}'.format(index,item), mode)
        selected = selected + key_action(stdscreen)
        if selected < 0:
            selected = 0
        if selected >= len(items):
            selected = len(items)-1
        stdscreen.refresh()

def key_action(stdscreen):
    key = stdscreen.getch()
    if key == ord('q'):
        quit()
    elif key in [curses.KEY_DOWN, ord('j')]:
        return 1
    elif key in [curses.KEY_UP, ord('k')]:
        return -1
    else:
        return 0
