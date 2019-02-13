import unittest
from games.tetris import car
from games.tetris import get_car_array

class TestTetris(unittest.TestCase):
    def test_get_car_array(self):
        hero = car(y=0, x = 0)
        expected = [[0,1],
                [1,0],[1,1],[1,2],
                [2,1],
                [3,0], [3,1],[3,2]]
        actual = get_car_array(hero)
        self.assertEqual(expected, actual)
