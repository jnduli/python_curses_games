import curses


class Car():
    CAR_WIDTH = 3
    CAR_HEIGHT = 4

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def body(self):
        """Returns list with coordinates on which to draw parts of car """
        y = self.y
        x = self.x
        return [
                [y, x+1],
                [y+1, x], [y+1, x+1], [y+1, x+2],
                [y+2, x+1],
                [y+3, x], [y+3, x+1], [y+3, x+2],
                ]

    def bounding_box(self):
        """Returns list with coordinates of the car bounding box"""
        y = self.y
        x = self.x
        upper_left = [y, x]
        upper_right = [y, x+self.CAR_WIDTH]
        lower_left = [y+self.CAR_HEIGHT, x]
        lower_right = [y+self.CAR_HEIGHT, x+self.CAR_WIDTH]
        return [upper_left, upper_right, lower_left, lower_right]

    def is_point_in_car(self, point):
        """Checks if point is within the car coordinates"""
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
        """Clears car from screen then adjusts the car's coordinates"""
        if window:
            self.clear(window)
        self.y = y
        self.x = x
