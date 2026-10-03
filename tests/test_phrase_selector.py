import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from phrase_selector import (
    build_fragment_candidates,
    normalize_phrase,
    select_random_fragment,
)


class TestPhraseSelector(unittest.TestCase):

    def test_normalize_phrase(self):
        self.assertEqual(
            normalize_phrase(
                "하늘이 열린다! 123"
            ),
            "하늘이열린다",
        )

    def test_fragment_length(self):
        phrases = [
            "바람이 불어오는 곳",
            "오늘은 새로운 날",
        ]

        for _ in range(30):
            fragment = select_random_fragment(
                phrases,
                min_length=3,
                max_length=5,
            )

            self.assertGreaterEqual(
                len(fragment),
                3,
            )

            self.assertLessEqual(
                len(fragment),
                5,
            )

    def test_require_shift(self):
        phrases = [
            "하늘과 바다가 만난다",
        ]

        candidates = build_fragment_candidates(
            phrases,
            min_length=3,
            max_length=5,
            require_shift=True,
        )

        self.assertTrue(
            candidates
        )

    def test_no_shift_candidate(self):
        phrases = [
            "하늘",
            "우리",
            "오늘",
            "마음",
        ]

        with self.assertRaises(ValueError):
            select_random_fragment(
                phrases,
                require_shift=True,
            )


if __name__ == "__main__":
    unittest.main()