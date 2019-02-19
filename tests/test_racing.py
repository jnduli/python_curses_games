import unittest
from games.race.car import Car

class TestRacing(unittest.TestCase):
    def test_get_car_body(self):
        hero = Car(y=0, x = 0)
        expected = [[0,1],
                [1,0],[1,1],[1,2],
                [2,1],
                [3,0], [3,1],[3,2]]
        actual = hero.body()
        self.assertEqual(expected, actual)
    
    def test_generate_car_bounds(self):
        hero = Car(y=0, x=0)
        expected = [[0,0], [0,3], [4,0], [4,3]]
        actual = hero.bounding_box() 
        self.assertEqual(expected, actual)
    
    def test_check_in_rectangle(self):
        hero = Car(y=0, x=0)
        point = [2,1]
        self.assertTrue(hero.is_point_in_car(point))
        point = [2,0]
        self.assertTrue(hero.is_point_in_car(point))
        point = [2,5]
        self.assertFalse(hero.is_point_in_car(point))
