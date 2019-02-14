import unittest
from games.tetris import rotate_object
from games.tetris import zed
from games.tetris import point

class TestTetris(unittest.TestCase):
    def test_zed(self):
        p = point(y=5, x = 10)
        expected = {
                'shape': [[5,10],[5,11],[6,11], [6,12]],
                'boundingbox': [[5,10], [5,12], [6,10], [6, 12]]
                }
        actual = zed(p)
        self.assertEqual(actual, expected)

    def test_rotate_object(self):
        p = point(y=5, x = 10)
        local_zed = zed(p)
        actual_shape, actual_bb = rotate_object(local_zed['shape'], local_zed['boundingbox'])
        expected_bb = [[6.5, 10.5], [4.5, 10.5], [6.5, 11.5], [4.5, 11.5]]
        self.assertEqual(actual_bb, expected_bb)
        expected_shape = [[6.5, 10.5], [5.5, 10.5], [5.5, 11.5], [4.5, 11.5]]
        self.assertEqual(actual_shape, expected_shape)
