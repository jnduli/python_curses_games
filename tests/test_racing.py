import unittest
from games.race.car import Car
from games.race.villains import Villains


class Window():
    """Mock object that emulates curses functionality"""

    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width

    def addch(self, *args):
        pass

    def getmaxyx(self):
        return (self.height, self.width)


class TestCar(unittest.TestCase):

    def test_get_car_body(self):
        hero = Car(y=0, x=0)
        expected = [[0, 1],
                    [1, 0], [1, 1], [1, 2],
                    [2, 1],
                    [3, 0], [3, 1], [3, 2]]
        actual = hero.body()
        self.assertEqual(expected, actual)

    def test_generate_car_bounds(self):
        hero = Car(y=0, x=0)
        expected = [[0, 0], [0, 3], [4, 0], [4, 3]]
        actual = hero.bounding_box()
        self.assertEqual(expected, actual)

    def test_check_in_rectangle(self):
        hero = Car(y=0, x=0)
        point = [2, 1]
        self.assertTrue(hero.is_point_in_car(point))
        point = [2, 0]
        self.assertTrue(hero.is_point_in_car(point))
        point = [2, 5]
        self.assertFalse(hero.is_point_in_car(point))

    def test_move(self):
        hero = Car(y=0, x=0)
        window = Window()
        hero.move(window, y=3, x=2)
        self.assertEqual(hero.x, 2)
        self.assertEqual(hero.y, 3)


class TestVillains(unittest.TestCase):

    def setUp(self):
        villains = Villains([1, 5, 9])
        villains.villains.append(Car(28, 1))
        villains.villains.append(Car(15, 5))
        villains.villains.append(Car(0, 1))
        self.villains = villains
        self.window = Window(height=30, width=13)

    def test_remove_villains(self):
        self.assertEqual(self.villains.remove(self.window), 1)
        self.assertEqual(self.villains.remove(self.window), 0)
        self.assertEqual(len(self.villains), 2)

    def test_move_villains(self):
        self.villains.move(self.window)
        expected_y = [29, 16, 1]
        for v in zip(self.villains, expected_y):
            self.assertEqual(v[0].y, v[1])
