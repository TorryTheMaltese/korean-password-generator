import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from hangul_transformer import (
    contains_shift_candidate,
    contains_shift_input,
    get_shift_transformations,
    transform_random_shift,
)


class TestHangulTransformer(unittest.TestCase):

    def test_existing_shift_input(self):
        self.assertTrue(contains_shift_input("예쁜"))

        self.assertTrue(contains_shift_input("쌀"))

    def test_no_shift_input(self):
        self.assertFalse(contains_shift_input("하늘"))

    def test_shift_candidate(self):
        self.assertTrue(contains_shift_candidate("바다"))

        self.assertTrue(contains_shift_candidate("배"))

    def test_no_shift_candidate(self):
        self.assertFalse(contains_shift_candidate("하늘"))

    def test_multiple_shift_transformations(self):
        transformations = set(get_shift_transformations("배"))

        self.assertEqual(
            transformations,
            {"빼", "뱨", "뺴"},
        )

    def test_existing_shift_text_is_preserved(self):
        self.assertEqual(
            transform_random_shift("예쁜"),
            "예쁜",
        )

    def test_transform_impossible_text(self):
        with self.assertRaises(ValueError):
            transform_random_shift("하늘")


if __name__ == "__main__":
    unittest.main()
