import curses
import random
from collections import namedtuple

car = namedtuple('Car', ['y', 'x'])

def get_car_array (car):
    '''
    Returns an array containing [y,x] values on 
    which to draw the parts of the car
    '''
    y = car.y
    x = car.x
    return [
            [y,x+1], 
            [y+1, x], [y+1, x+1], [y+1, x+2],
            [y+2, x+1],
            [y+3, x], [y+3, x+1], [y+3, x+2],
            ] 

def paint_car(window, car, character):
    '''
    Draws the car with the selected character provided
    '''
    for coord in get_car_array(car):
        window.addch(*coord, character)

def draw_car(window, car):
    paint_car(window, car, curses.ACS_CKBOARD)

def clear_car(window, car):
    paint_car(window, car, ' ')

#TODO: fix this up to prevent unwinable situations
def generate_villain(hero, villains):
    allowed_x = [1, 5, 9]
    # 20 % change of villain generation
    generate = random.randint(1,5) % 5 == 0
    if not generate:
        return None
    villain = car(y=random.randint(0,20), x=allowed_x[random.randint(0,2)])
    if check_for_collisions(hero, [villain]):
        return None
    return villain

#TODO: control the speed of motion of villains
def move_villains(window, villains):
    new_villains = []
    for v in villains:
        clear_car(window, v)
        new_v = car(v.y+1, v.x)
        draw_car(window, new_v)
        new_villains.append(new_v)
    return new_villains

def generate_car_bounds(car):
    """
    Generate [y,x] coordinates that show coordinates of car rectangle
    """
    upper_left = [car.y, car.x]
    upper_right = [car.y, car.x + 3]
    lower_left = [car.y + 4, car.x]
    lower_right = [car.y + 4, car.x + 3]
    return [upper_left, upper_right, lower_left, lower_right]

def check_in_rectangle(car, point):
    [car_y, car_x] = car
    [y, x] = point
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

def remove_old_cars(window, villains):
    height,_ = window.getmaxyx()
    new_villains = []
    for car in villains:
        if car.y < (height-4):
            new_villains.append(car)
        else:
            clear_car(window, car)
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
    hero = car(y=height//2, x=width//3 + 1)
    left_limit = 1 
    right_limit = width - 4
    villains = []
    while key is not ord('q'):
        key = window.getch()
        villain = generate_villain(hero, villains)
        if villain:
            villains.append(villain)
        draw_car(window, hero)
        new_x = hero_motion(key) * 4 + hero[1]
        if new_x < left_limit:
            new_x = left_limit
        if new_x > right_limit:
            new_x = right_limit
        if hero[1] is not new_x:
            clear_car(window, hero)
            hero = car(hero.y, new_x)
        villains = move_villains(window, villains)
        if (check_for_collisions(hero, villains)):
            return
        villains = remove_old_cars(window, villains)

def hero_motion(key):
    if key in [curses.KEY_LEFT, ord('h')]:
        return -1
    elif key in [curses.KEY_RIGHT, ord('l')]:
        return 1
    else:
        return 0
