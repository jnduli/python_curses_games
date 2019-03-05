import unittest
from games.tetris.tetris import rotate_object
from games.tetris.shapes import Zed
from games.tetris.shapes import Point


class TestShapes(unittest.TestCase):

    def test_zed(self):
        z = Zed(y=5, x=10)
        expected = {
                'shape': [Point(5, 10), Point(5, 11),
                          Point(6, 11), Point(6, 12)],
                'boundingbox': [Point(5, 10), Point(5, 12),
                                Point(6, 10), Point(6, 12)]
                }
        self.assertEqual(z.shape, expected['shape'])
        self.assertEqual(z.boundingbox, expected['boundingbox'])

    def test_rotate_zed(self):
        z = Zed(y=5, x=10)
        z.rotate_clockwise()
        expected_bb = [Point(6.5, 10.5), Point(4.5, 10.5),
                       Point(6.5, 11.5), Point(4.5, 11.5)]
        self.assertEqual(z.boundingbox, expected_bb)
        expected_shape = [Point(6.5, 10.5), Point(5.5, 10.5),
                          Point(5.5, 11.5), Point(4.5, 11.5)]
        self.assertEqual(z.shape, expected_shape)


#  class TestTetris(unittest.TestCase):
#
    #  def test_rotate_object(self):
        #  p = point(y=5, x = 10)
        #  local_zed = zed(p)
        #  actual_shape, actual_bb = rotate_object(local_zed['shape'], local_zed['boundingbox'])
        #  expected_bb = [[6.5, 10.5], [4.5, 10.5], [6.5, 11.5], [4.5, 11.5]]
        #  self.assertEqual(actual_bb, expected_bb)
        #  expected_shape = [[6.5, 10.5], [5.5, 10.5], [5.5, 11.5], [4.5, 11.5]]
        #  self.assertEqual(actual_shape, expected_shape)
