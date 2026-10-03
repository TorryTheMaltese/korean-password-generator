import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):

    def test_valid_password(self):
        result = validate_password(
            "Rkakemr34##"
        )

        self.assertTrue(
            result.is_valid
        )

        self.assertTrue(
            result.has_uppercase
        )

        self.assertTrue(
            result.has_lowercase
        )

        self.assertTrue(
            result.has_digit
        )

        self.assertTrue(
            result.has_special
        )

    def test_missing_uppercase(self):
        result = validate_password(
            "abcdef12!"
        )

        self.assertFalse(
            result.is_valid
        )

        self.assertIn(
            "영문 대문자가 1개 이상 필요합니다.",
            result.errors,
        )

    def test_missing_digit(self):
        result = validate_password(
            "Abcdefgh!"
        )

        self.assertFalse(
            result.is_valid
        )

        self.assertIn(
            "숫자가 1개 이상 필요합니다.",
            result.errors,
        )

    def test_too_short(self):
        result = validate_password(
            "Ab1!"
        )

        self.assertFalse(
            result.is_valid
        )

        self.assertIn(
            "최소 8자 이상이어야 합니다.",
            result.errors,
        )


if __name__ == "__main__":
    unittest.main()