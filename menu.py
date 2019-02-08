import curses

def menu(stdscreen):
    stdscreen.clear()
    items = ['Snake', 'Tetris(Not implemented)', 'Typing Tutor(Not Implemented)']
    display(stdscreen, items)

def display(stdscreen, items, menu_y=5):
    while True:
        for index, item in enumerate(items):
            stdscreen.addstr(menu_y + index, 1, '{}. {}'.format(index,item))
        stdscreen.refresh()
