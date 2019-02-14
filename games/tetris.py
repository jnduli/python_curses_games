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
    return [shape, boundingbox]

def l (point):
    y = point.y
    x = point.x
    shape = [
            [y,x],
            [y+1, x],
            [y+2, x], [y+2, x+1] 
            ]
    boundingbox = [[y,x], [y,x+1], [y+2], [x+1]]
    return [shape, boundingbox]

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

    screen_blocks = [[0 for i in range(0, SCREEN_WIDTH)] for i in range (0, height)]
    key = 0
    some = point(y=0, x=width//3 + 1)
    shape = None
    boundingbox = None
    while key is not ord('q'):
        if (shape is None):
            shape, boundingbox = zed(some)
        key = window.getch()
        clear_letter(window, shape)
        shape, boundingbox = key_motion(key, shape, boundingbox)
        shape, boundingbox = move_down(shape, boundingbox)
        if (int(boundingbox[2][0]) >= (height-1) or check_shape_touched_floor(screen_blocks, shape)):
            for coord in shape:
                coord = [int(a) for a in coord]
                screen_blocks[coord[0]][coord[1]] = 1
            shape = None
            boundingbox = None
            continue
        draw_letter(window, shape)
        draw_blocks(window, screen_blocks)

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
def key_motion(key, shape, boundingbox):
    if key is ord('r'):
        shape,boundingbox = rotate_object(shape, boundingbox)
    elif key in [curses.KEY_LEFT, ord('h')]:
        shape = [[coord[0], coord[1]-1] for coord in shape]
        boundingbox = [[coord[0], coord[1]-1] for coord in boundingbox]
    elif key in [curses.KEY_RIGHT, ord('l')]:
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
