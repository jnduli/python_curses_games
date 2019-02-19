import curses
import random
from collections import namedtuple

car = namedtuple('Car', ['y', 'x'])
class Car():
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def body(self):
        '''
        Returns an array containing [y,x] values on 
        which to draw the parts of the car
        '''
        y = self.y
        x = self.x
        return [
                [y, x+1], 
                [y+1, x], [y+1, x+1], [y+1, x+2],
                [y+2, x+1],
                [y+3, x], [y+3, x+1], [y+3, x+2],
                ] 

    def bounding_box(self):
        """
        Generate [y,x] coordinates that show coordinates of car rectangle
        """
        y = self.y
        x = self.x
        upper_left = [y, x]
        upper_right = [y, x + 3]
        lower_left = [y + 4, x]
        lower_right = [y + 4, x + 3]
        return [upper_left, upper_right, lower_left, lower_right]

    def is_point_in_car(self, point):
        '''
        Checks if the point is within the car coordinates
        '''
        [ul, ur, ll, lr] = self.bounding_box()
        [y, x] = point

        if (x >= ul[1] and x <= ur[1] and y >= ul[0] and y <= ll[0]):
            return True
        return False
    
    def draw(self, window):
        for coord in self.body():
            window.addch(*coord, curses.ACS_CKBOARD)

    def clear(self, window):
        for coord in self.body():
            window.addch(*coord, ' ')

    def move(self, window, y, x):
        self.clear(window)
        self.y = y
        self.x = x


#TODO: fix this up to prevent unwinable situations
def generate_villain(hero, villains):
    allowed_x = [1, 5, 9]
    # 20 % change of villain generation
    generate = random.randint(1,2) % 1 == 0
    if not generate:
        return None
    villain = Car(y=random.randint(0,5), x=allowed_x[random.randint(0,2)])
    if check_for_collisions(hero, [villain]):
        return None
    if not villains:
        return villain
    last_villain = villains[-1]
    if check_for_collisions(villain, [last_villain]):
        return None
    if (villain.x == 5 or villain.x !=5) and (villain.y + 9) > last_villain.y:
        return None
    return villain

#TODO: control the speed of motion of villains
def move_villains(window, villains):
    for v in villains:
        v.move(window, v.y+1, v.x)
    return villains


def check_for_collisions(hero, villains):
    hero_points = hero.bounding_box()
    for v in villains:
        for point in hero_points:
            if v.is_point_in_car(point):
                return True
    return False

def remove_old_cars(window, villains):
    height,_ = window.getmaxyx()
    new_villains = []
    for car in villains:
        if car.y < (height-4):
            new_villains.append(car)
            car.draw(window)
        else:
            car.clear(window)
    return new_villains
    
def create_score_board(stdscreen):
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, 13, 0 , width//2)
    window.keypad(1)
    window.timeout(100)
    window.border(0,0,0,0,0,0,0,0)
    return window

def create_game_board(stdscreen):
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, width//2 - 20, 0 , width//2 + 14)
    window.border(0,0,0,0,0,0,0,0)
    window.addstr(height//4, 1, 'Press q to leave racing game')
    window.refresh()
    return window

def updateScore(scoreWindow, score):
    scoreMessage = 'Score: {}'.format(score)
    height, width = scoreWindow.getmaxyx()
    scoreWindow.addstr(height//2, width//2, scoreMessage)
    scoreWindow.refresh()

def racing(stdscreen):
    curses.curs_set(0)
    window = create_score_board(stdscreen)
    height, width = window.getmaxyx()
    score_window = create_game_board(stdscreen)
    key = 0
    hero = Car(y=(height*3)//5, x=width//3 + 1)
    left_limit = 1 
    right_limit = width - 4
    villains = []
    score = 0
    while key is not ord('q'):
        key = window.getch()
        villain = generate_villain(hero, villains)
        if villain:
            villains.append(villain)
        hero.draw(window)
        new_x = hero_motion(key) * 4 + hero.x
        if new_x < left_limit:
            new_x = left_limit
        if new_x > right_limit:
            new_x = right_limit
        if hero.x is not new_x:
            hero.move(window, y=hero.y, x = new_x)
        villains = move_villains(window, villains)
        if (check_for_collisions(hero, villains)):
            return
        before_clear = len(villains)
        villains = remove_old_cars(window, villains)
        after_clear = len(villains)
        score = score + (before_clear - after_clear )
        updateScore(score_window, score)

def hero_motion(key):
    if key in [curses.KEY_LEFT, ord('h')]:
        return -1
    elif key in [curses.KEY_RIGHT, ord('l')]:
        return 1
    else:
        return 0
