from utils import get_overlapping_circles, new_circle_is_overlapping_existing_circles
import unittest
from parameterized import parameterized

class UtilsTests(unittest.TestCase):

    @parameterized.expand([
        [
            [[1,1,0],[4,5,1],[10,3,2]],
            [[1,1,3],[5,5,4],[12,4,5]],
            1,
            [3]
        ],
        [
            [[1,1,0],[4,5,1],[10,3,2]],
            [[1,2,3],[5,5,4],[12,4,5]],
            1,
            []
        ],
        [
            [[1,1,0],[4,5,1],[10,3,2]],
            [[1,2,3],[5,5,4], [12,4,5]],
            2,
            [3,4]
        ]
    ])
    def test_get_overlapping_circles(self, first, second, diameter, expected_circles_to_remove):
        circles_to_remove = get_overlapping_circles(first, second, diameter)
        self.assertEqual(circles_to_remove, expected_circles_to_remove)

    @parameterized.expand([
        [
            1,
            1,
            [[1,2,0],[4,7,1]],
            1,
            False
        ],
        [
            1,
            1,
            [[1,1.345,0],[4,7,1]],
            1,
            True
        ],
        [
            1,
            1,
            [[1,2,0],[0.3,1.1,1]],
            1,
            True
        ]
    ])
    def test_new_circle_is_overlapping_existing_circles(self, x, y, existing_circles, diameter, is_overlapping):
        self.assertEqual(new_circle_is_overlapping_existing_circles(x, y, existing_circles, diameter), is_overlapping)

