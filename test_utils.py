from utils import get_overlapping_circles, new_circle_is_overlapping_existing_circles
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
        [
            1,
            1,
            [[1,2],[4,7]],
            0.5,
            False
        ],
        [
            1,
            1,
            [[1,1.345],[4,7]],
            0.5,
            True
        ],
        [
            1,
            1,
            [[1,2],[0.3,1.1]],
            0.5,
            True
        ]
    ])
    def test_new_circle_is_overlapping_existing_circles(self, x, y, existing_circles, radius, is_overlapping):
        self.assertEqual(new_circle_is_overlapping_existing_circles(x, y, existing_circles, radius), is_overlapping)

