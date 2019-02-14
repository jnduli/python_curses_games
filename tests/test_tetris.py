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
        actual = rotate_object(local_zed['shape'], local_zed['boundingbox'])
        expected = [[-0.5, -1], [-0.5, 1], [0.5, -1], [0.5, 1]]
        self.assertEqual(actual, expected)
