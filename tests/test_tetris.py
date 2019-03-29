import unittest
from games.tetris.shapes import Zed, L, Box, Tee
from games.tetris.shapes import Point
from games.tetris.tetris import ScreenBlocks
from .test_racing import Window


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
        z.rotate_clockwise(Window(), 20, 0)
        expected_bb = [Point(4.5, 10.5), Point(4.5, 11.5),
                       Point(6.5, 10.5), Point(6.5, 11.5)]
        self.assertEqual(z.boundingbox, expected_bb)
        expected_shape = [Point(6.5, 10.5), Point(5.5, 10.5),
                          Point(5.5, 11.5), Point(4.5, 11.5)]
        self.assertEqual(z.shape, expected_shape)

    def test_L(self):
        l_shape = L(y=5, x=5)
        expected_shape = [
                Point(5, 5),
                Point(6, 5),
                Point(7, 5), Point(7, 6)
                ]
        self.assertEqual(l_shape.shape, expected_shape)
        expected_bb = [
                Point(5, 5), Point(5, 6),
                Point(7, 5), Point(7, 6)
                ]
        self.assertEqual(l_shape.boundingbox, expected_bb)

    def test_box(self):
        box = Box(y=5, x=5)
        expected_shape = [
                Point(5, 5), Point(5, 6),
                Point(6, 5), Point(6, 6)
                ]
        self.assertEqual(box.shape, expected_shape)
        self.assertEqual(box.boundingbox, expected_shape)

    def test_tee(self):
        tee = Tee(y=5, x=5)
        expected_shape = [
                Point(5, 5),
                Point(6, 5), Point(6, 6),
                Point(7, 5)
                ]
        self.assertEqual(tee.shape, expected_shape)
        expected_bb = [
                Point(5, 5), Point(5, 6),
                Point(7, 5), Point(7, 6)
                ]
        self.assertEqual(tee.boundingbox, expected_bb)


class TestScreenBlocks(unittest.TestCase):

    def test_create_screen_blocks(self):
        expected = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        sb = ScreenBlocks(3, 3, 1)
        self.assertEqual(sb.shape, expected)

    def test_clear_and_score(self):
        sb = ScreenBlocks(3, 3, 1)
        new_shape = [[0, 0, 0, 0],[0, 0, 1, 0], [0, 1, 1, 0]]
        sb.shape = new_shape
        score = sb.clear_and_score()
        self.assertEqual(score, 1)
        expected_shape = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]]
        self.assertEqual(sb.shape, expected_shape)
        sb.shape[2][1] = 1
        score = sb.clear_and_score()
        self.assertEqual(score, 2)
        expected_shape = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(sb.shape, expected_shape)
