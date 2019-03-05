from collections import deque
import random
from .collisions import Collision
from .car import Car


class Villains(Collision):
    def __init__(self, x_positions):
        self.villains = deque()
        self.allowed_x = x_positions

    def __getitem__(self, index):
        return self.villains[index]

    def __len__(self):
        return len(self.villains)

    def random_add(self, hero, difficulty=1):
        """Randomly generates villains 70% of the time per call"""
        generate = random.randint(0, 10) < 7
        villain = Car(y=0,
                      x=self.allowed_x[random.randint(0, 2)])
        if not generate:
            return

        try:
            last_villain = self.villains[-1]
            # Makes sure the generated villain and last villain don't collide
            if self.check_for_collisions(villain, [last_villain]):
                return
            second_last_villain = self.villains[-2]
            # Preventing three heros on a row
            # Generate villain if there is enough space for hero to manoeuvre 
            # However this prevents two heros following each other
            generate_double = random.randint(0, 10) < difficulty 
            if (generate_double
                    and last_villain.y+Car.CAR_HEIGHT >= second_last_villain.y
                    and villain.y + 9 > last_villain.y):
                return
            if (not generate_double and villain.y +9 > last_villain.y):
                return

            self.villains.append(villain)
        except IndexError:
            self.villains.append(villain)

    # TODO: control the speed of motion of villains
    def move(self, window):
        for v in self.villains:
            v.move(window, v.y+1, v.x)

    def remove(self, window):
        """Remove first car if it's beyond window height"""
        height, _ = window.getmaxyx()
        try:
            first_villain = self.villains[0]
            if (first_villain.y >= height - 4):
                self.villains.popleft().clear(window)
                return 1
            return 0
        except IndexError:
            return 0

    def draw(self, window):
        for car in self.villains:
            car.draw(window)
