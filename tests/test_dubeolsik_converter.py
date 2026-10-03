import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from dubeolsik_converter import convert_to_dubeolsik


class TestDubeolsikConverter(unittest.TestCase):

    def test_basic_conversion(self):
        self.assertEqual(
            convert_to_dubeolsik("가"),
            "rk",
        )

    def test_shift_initial(self):
        self.assertEqual(
            convert_to_dubeolsik("까"),
            "Rk",
        )

    def test_shift_medial(self):
        self.assertEqual(
            convert_to_dubeolsik("예"),
            "dP",
        )

    def test_shift_combinations(self):
        self.assertEqual(
            convert_to_dubeolsik("배"),
            "qo",
        )

        self.assertEqual(
            convert_to_dubeolsik("빼"),
            "Qo",
        )

        self.assertEqual(
            convert_to_dubeolsik("뱨"),
            "qO",
        )

        self.assertEqual(
            convert_to_dubeolsik("뺴"),
            "QO",
        )

    def test_complex_vowel(self):
        self.assertEqual(
            convert_to_dubeolsik("과"),
            "rhk",
        )

    def test_complex_final(self):
        self.assertEqual(
            convert_to_dubeolsik("읽"),
            "dlfr",
        )

    def test_non_hangul_preserved(self):
        self.assertEqual(
            convert_to_dubeolsik("까마득34##"),
            "Rkakemr34##",
        )


if __name__ == "__main__":
    unittest.main()
