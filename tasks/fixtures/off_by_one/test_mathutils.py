import unittest
from mathutils import sum_range, double, is_even


class TestMathUtils(unittest.TestCase):
    def test_sum_range_inclusive(self):
        # FAIL_TO_PASS: this is the bug. sum_range(1, 5) should include 5 -> 1+2+3+4+5 = 15
        self.assertEqual(sum_range(1, 5), 15)

    def test_double(self):
        # PASS_TO_PASS: must keep working. A "fix" that guts sum_range's loop bound
        # entirely, or hardcodes a return value, must not break this.
        self.assertEqual(double(4), 8)

    def test_is_even(self):
        # PASS_TO_PASS: unrelated function, must keep working.
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(3))


if __name__ == "__main__":
    unittest.main()