
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
    boundingbox = [[y,x], [y,x+1], [y+2, x], [y+2, x+1]]
    return [shape, boundingbox]

def box (point):
    y = point.y
    x = point.x
    shape = [
            [y,x],[y, x+1],
            [y+1, x], [y+1, x+1]
            ]
    return [shape, shape]
