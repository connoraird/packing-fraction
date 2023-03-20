from utils import get_overlapping_circles, circles_are_overlapping
import unittest
from parameterized import parameterized

class UtilsTests(unittest.TestCase):

    @parameterized.expand([
        [
            [[1,1],[4,5],[10,3]],
            [[1,1], [5,5], [12,4]],
            0.5,
            [[1,1]]
        ],
        [
            [[1,1],[4,5],[10,3]],
            [[1,2], [5,5], [12,4]],
            0.5,
            []
        ],
        [
            [[1,1],[4,5],[10,3]],
            [[1,2], [5,5], [12,4]],
            1,
            [[1,2],[5,5]]
        ]
    ])
    def test_get_overlapping_circles(self, first, second, radius, expected_circles_to_remove):
        circles_to_remove = get_overlapping_circles(first, second, radius)
        self.assertEqual(circles_to_remove, expected_circles_to_remove)

    @parameterized.expand([
        [1, 2, 3, 4, 1, False],
        [1, 2, 1, 2, 1, True],
        [1, 2, 2, 2, 1, True]
    ])
    def test_circles_are_overlapping(self, x1, y1, x2, y2, radius, is_overlapping):
        self.assertEqual(circles_are_overlapping(x1, y1, x2, y2, radius), is_overlapping)

