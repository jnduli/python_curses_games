import unittest
from games.tetris import car
from games.tetris import get_car_array
from games.tetris import generate_car_bounds
from games.tetris import check_in_rectangle

class TestTetris(unittest.TestCase):
    def test_get_car_array(self):
        hero = car(y=0, x = 0)
        expected = [[0,1],
                [1,0],[1,1],[1,2],
                [2,1],
                [3,0], [3,1],[3,2]]
        actual = get_car_array(hero)
        self.assertEqual(expected, actual)
    
    def test_generate_car_bounds(self):
        hero = car(y=0, x=0)
        expected = [[0,0], [0,3], [4,0], [4,3]]
        actual = generate_car_bounds(hero) 
        self.assertEqual(expected, actual)
    
    def test_check_in_rectangle(self):
        hero = car(y=0, x=0)
        point = [2,1]
        self.assertTrue(check_in_rectangle(hero, point))
        point = [2,0]
        self.assertTrue(check_in_rectangle(hero, point))
        point = [2,5]
        self.assertFalse(check_in_rectangle(hero, point))
