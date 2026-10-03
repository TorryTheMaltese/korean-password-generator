import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from password_generator import generate_password


class TestPasswordGenerator(unittest.TestCase):

    def test_generated_password_is_valid(self):
        phrases = [
            "까마득한 날에",
            "바람이 부는 날",
            "새로운 길을 걷는다",
            "푸른 바다를 바라본다",
        ]

        for _ in range(50):
            result = generate_password(
                phrases
            )

            self.assertTrue(
                result.validation.is_valid,
                msg=(
                    f"생성 실패: "
                    f"{result.display_text} / "
                    f"{result.actual_password} / "
                    f"{result.validation.errors}"
                ),
            )

    def test_no_shift_source_fails(self):
        phrases = [
            "하늘",
            "우리",
            "오늘",
            "마음",
        ]

        with self.assertRaises(ValueError):
            generate_password(
                phrases
            )


if __name__ == "__main__":
    unittest.main()