import curses

MOTION = 3
def get_car_array (y, x):
    return [
            [y,x+1], 
            [y+1, x], [y+1, x+1], [y+1, x+2],
            [y+2, x+1],
            [y+3, x], [y+3, x+1], [y+3, x+2],
            ] 

def draw_car(window, y, x):
    for coord in get_car_array(y,x):
        window.addch(*coord, curses.ACS_CKBOARD)

def clear_car(window, y, x):
    for coord in get_car_array(y, x):
        window.addch(*coord, ' ')

def generate_villain():
    return [[0, 1], [7, 9]]

def move_villains(window, villains):
    for car in villains:
        clear_car(window, *car)
        car[0] = car[0] + 1
        draw_car(window, *car)
    return villains
    

def tetris(stdscreen):
    curses.curs_set(0)
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, 13, 0 , width//2)
    height, width = window.getmaxyx()
    window.keypad(1)
    window.timeout(100)
    window.border(0,0,0,0,0,0,0,0)
    key = 0
    hero = [height//2, width//3 + 1]
    left_limit = 1 
    right_limit = width - 4
    villains = generate_villain()
    while key is not ord('q'):
        key = window.getch()
        draw_car(window, *hero)
        new_x = hero_motion(key) * 4 + hero[1]
        if new_x < left_limit:
            new_x = left_limit
        if new_x > right_limit:
            new_x = right_limit
        if hero[1] is not new_x:
            clear_car(window, *hero)
            hero[1] = new_x
        move_villains(window, villains)
        #  car(window, height//2, width//2)

def hero_motion(key):
    if key in [curses.KEY_LEFT, ord('h')]:
        return 1
    elif key in [curses.KEY_RIGHT, ord('l')]:
        return -1
    else:
        return 0
