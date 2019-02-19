import curses

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
        #  return self
