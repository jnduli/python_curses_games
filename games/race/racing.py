import curses
import random
from collections import namedtuple
from .car import Car
from .villains import Villains
import time


def check_for_collisions(hero, villains):
    hero_points = hero.bounding_box()
    for v in villains:
        for point in hero_points:
            if v.is_point_in_car(point):
                return True
    return False

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
    villains = Villains() 
    score = 0
    prev_time = time.time_ns()
    while key is not ord('q'):
        key = window.getch()
        villains.random_add(hero)
        hero.draw(window)
        villains.move(window)
        villains.draw(window)
        new_x = hero_motion(key) * 4 + hero.x
        if new_x < left_limit:
            new_x = left_limit
        if new_x > right_limit:
            new_x = right_limit
        if hero.x is not new_x:
            hero.move(window, y=hero.y, x = new_x)
        if (check_for_collisions(hero, villains)):
            return
        before_clear = len(villains)
        villains.remove(window)
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
