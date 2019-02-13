import curses
import random
from collections import namedtuple

car = namedtuple('Car', ['y', 'x'])

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

def generate_villain(hero):
    allowed_x = [1, 5, 9]
    generate = random.randint(1,9) % 4 == 0
    if generate:
        villain = [random.randint(0,20), allowed_x[random.randint(0,2)]]
        if check_for_collisions(hero, [villain]):
            return None
        return villain
    return None

def move_villains(window, villains):
    for car in villains:
        clear_car(window, *car)
        car[0] = car[0] + 1
        draw_car(window, *car)
    return villains

def generate_car_bounds(car):
    return [car, [car[0], car[1]+3],[car[0]+4, car[1]], [car[0]+4, car[1] + 3]]

def check_in_rectangle(car, point):
    car_x = car[1]
    car_y = car[0]
    y = point[0]
    x = point[1]
    if (x >= car_x and x <= (car_x + 3) and y >= car_y and y <= (car_y +4)):
        return True
    return False

def check_for_collisions(hero, villains):
    hero_points = generate_car_bounds(hero)
    for v in villains:
        for point in hero_points:
            if check_in_rectangle(v, point):
                return True
    return False

def remove_old_cars(window, villains, height):
    new_villains = []
    for car in villains:
        if car[0] < (height-4):
            new_villains.append(car)
        else:
            clear_car(window, *car)
    return new_villains
    

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
    villains = []
    while key is not ord('q'):
        key = window.getch()
        villain = generate_villain(hero)
        if villain:
            villains.append(villain)
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
        if (check_for_collisions(hero, villains)):
            return
        villains = remove_old_cars(window, villains, height)

def hero_motion(key):
    if key in [curses.KEY_LEFT, ord('h')]:
        return -1
    elif key in [curses.KEY_RIGHT, ord('l')]:
        return 1
    else:
        return 0
