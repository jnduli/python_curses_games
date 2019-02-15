from collections import namedtuple
import curses
import random
import time
from .tetris_shapes import zed, l, box

point = namedtuple('Car', ['y', 'x'])

def get_random_shape(point):
    shapes = [zed, l, box]
    return shapes[random.randint(0,2)](point)

def draw_letter(window, points):
    for coord in points:
        window.addch(int(coord[0]), int(coord[1]), curses.ACS_CKBOARD)

def clear_letter(window, points):
    for coord in points:
        window.addch(int(coord[0]), int(coord[1]), ' ')

SCREEN_WIDTH = 25
DOWNWARDS_SPEED = 0.01 # number of characters to move down per second

def should_move(prevtime, downwards_speed=DOWNWARDS_SPEED):
    nanos = 1000000 / downwards_speed
    if (time.time_ns() - prevtime) >= nanos:
        return True
    return False

def tetris (stdscreen):
    curses.curs_set(0)
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, SCREEN_WIDTH, 0 , width//2)
    height, width = window.getmaxyx()
    window.keypad(1)
    window.timeout(41) # This is set to throttle cpu usage
    window.border(0,0,0,0,0,0,0,0)

    screen_blocks = [[0 for i in range(0, SCREEN_WIDTH)] for i in range (0, height-1)]
    key = 0
    some = point(y=0, x=width//3 + 1)
    shape = None
    boundingbox = None
    prev_time = time.time_ns()

    while key is not ord('q'):
        if (shape is None):
            shape, boundingbox = get_random_shape(some)
        key = window.getch()
        clear_letter(window, shape)
        shape, boundingbox = key_motion(key, shape, boundingbox, SCREEN_WIDTH-2, 1)
        if (should_move(prev_time)):
            shape, boundingbox = move_down(shape, boundingbox)
            prev_time = time.time_ns()

        if (int(boundingbox[2][0]) >= (height-2) or check_shape_touched_floor(screen_blocks, shape)):
            for coord in shape:
                coord = [int(a) for a in coord]
                screen_blocks[coord[0]][coord[1]] = 1
            shape = None
            boundingbox = None
            draw_blocks(window, screen_blocks)
            continue
        draw_letter(window, shape)

def check_shape_touched_floor(shape_blocks, shape):
    for coord in shape:
        coord = [int(a) for a in coord]
        if (coord[0]+1 >= len(shape_blocks)):
            continue
        next_layer = shape_blocks[coord[0]+1][coord[1]]
        if next_layer == 1:
            return True
    return False

def draw_blocks(window, shape_blocks):
    for y, row in enumerate(shape_blocks):
        for x, point in enumerate(row):
            if point == 1:
                draw_letter(window, [[y,x]])

# TODO: deal with limits here
def key_motion(key, shape, boundingbox, rightlimit, leftlimit=0):
    if key is ord('r'):
        shape,boundingbox = rotate_object(shape, boundingbox)
    elif key in [curses.KEY_LEFT, ord('h')] and (boundingbox[0][1]-1)>=leftlimit:
        shape = [[coord[0], coord[1]-1] for coord in shape]
        boundingbox = [[coord[0], coord[1]-1] for coord in boundingbox]
    elif key in [curses.KEY_RIGHT, ord('l')] and (boundingbox[1][1]+1) <= rightlimit:
        shape = [[coord[0], coord[1]+1] for coord in shape]
        boundingbox = [[coord[0], coord[1]+1] for coord in boundingbox]
    return [shape, boundingbox]

def move_down(shape, boundingbox):
    shape = [[coord[0]+1, coord[1]] for coord in shape]
    boundingbox = [[coord[0]+1, coord[1]] for coord in boundingbox]
    return [shape, boundingbox]

def rotate_object(shape, boundingbox):
    '''
    This does a matrix manipulation on all the points by
    [ 0 -1
      1 0 ]
      so as to achieve 90 degrees rotation
    '''
    bb_y = (boundingbox[0][0] + boundingbox[2][0]) / 2
    bb_x = (boundingbox[0][1] + boundingbox[1][1]) / 2
    return [get_new_rotated_coordinates(shape, bb_y, bb_x), get_new_rotated_coordinates(boundingbox, bb_y, bb_x)]

def get_new_rotated_coordinates(points, bb_y, bb_x):
    points_relative = [[coord[0] - bb_y, coord[1] - bb_x] for coord in points]
    return [rotate_point(*coord, bb_y, bb_x) for coord in points_relative] 

def rotate_point(y, x, origin_y=0, origin_x=0):
    '''
    Performs a 90 degree rotation about relative origin
    Then adds the vector to get coordinates in global system
    '''
    return [-x+origin_y, y+origin_x]
