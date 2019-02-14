from collections import namedtuple
import curses

point = namedtuple('Car', ['y', 'x'])

def zed(point):
    y = point.y
    x = point.x
    shape = [
            [y, x], [y, x+1],
            [y+1, x+1], [y+1, x+2]
            ]
    boundingbox = [[y,x], [y, x+2], [y+1,x], [y+1, x+2]]
    return {
            'shape': shape,
            'boundingbox': boundingbox
            }

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
        coord = [int(x) for x in coord]
        window.addch(*coord, curses.ACS_CKBOARD)

def clear_letter(window, points):
    for coord in points:
        coord = [int(x) for x in coord]
        window.addch(*coord, ' ')

SCREEN_WIDTH = 25
def tetris (stdscreen):
    curses.curs_set(0)
    height, width = stdscreen.getmaxyx()
    window = curses.newwin(height, SCREEN_WIDTH, 0 , width//2)
    height, width = window.getmaxyx()
    window.keypad(1)
    window.timeout(100)
    window.border(0,0,0,0,0,0,0,0)

    screen_blocks = [[0 for i in range(1, SCREEN_WIDTH)] for i in range (1, height)]
    key = 0
    some = point(y=10, x=width//3 + 1)
    shape = zed(some)['shape']
    boundingbox = zed(some)['boundingbox']
    while key is not ord('q'):
        key = window.getch()
        clear_letter(window, shape)
        some = point(y=some.y+1, x = some.x)
        #  shape = zed(some)['shape']
        draw_letter(window, shape)

def key_motion(key, shape, boundingbox):
    if key is ord('r'):
        shape,boundingbox = rotate_object(shape, boundingbox)
def rotate_object(shape, boundingbox):
    '''
    This does a matrix manipulation on all the points by
    [ 0 -1
      1 0 ]
      so as to achieve 90 degrees rotation
    '''
    bb_y = (boundingbox[0][0] + boundingbox[2][0]) / 2
    bb_x = (boundingbox[0][1] + boundingbox[1][1]) / 2
    bb_origin = [bb_y, bb_x]
    # Get relative coordinates of bounding box
    bb_relative = [[coord[0] - bb_origin[0], coord[1] - bb_origin[1]] for coord in boundingbox]
    new_bb_relative = [rotate_point(*coord) for coord in bb_relative] 
    new_bb = [[coord[0] + bb_origin[0], coord[1] + bb_origin[1]] for coord in new_bb_relative]
    # Get relative coordinates of shape
    shape_relative = [[coord[0] - bb_origin[0], coord[1] - bb_origin[1]] for coord in shape]
    new_shape_relative = [rotate_point(*coord) for coord in shape_relative] 
    new_shape = [[coord[0] + bb_origin[0], coord[1] + bb_origin[1]] for coord in new_shape_relative]
    return [new_shape, new_bb]

def rotate_point(y, x):
    return [-x, y]
