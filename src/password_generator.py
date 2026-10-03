from dataclasses import dataclass

from dubeolsik_converter import convert_to_dubeolsik
from hangul_transformer import (
    contains_shift_input,
    transform_random_shift,
)
from password_composer import compose_password_text
from password_validator import (
    ValidationResult,
    validate_password,
)
from phrase_selector import select_random_fragment


@dataclass(frozen=True)
class GeneratedPassword:
    """
    비밀번호 생성 결과.

    display_text:
        사용자가 기억하고 직접 입력할 한글 기반 문자열.

    actual_password:
        내부 검증용 실제 두벌식 키 입력 문자열.

    validation:
        복잡도 검증 결과.
    """

    display_text: str
    actual_password: str
    validation: ValidationResult


def generate_password(
    phrases: list[str],
    *,
    min_fragment_length: int = 3,
    max_fragment_length: int = 5,
    require_uppercase: bool = True,
    min_password_length: int = 8,
) -> GeneratedPassword:
    """
    최종 비밀번호 후보를 생성하고 검증한다.

    기본 설정에서는 영문 대문자가 포함되도록
    Shift 입력 가능한 한글 문자열만 선택한다.
    """

    fragment = select_random_fragment(
        phrases,
        min_length=min_fragment_length,
        max_length=max_fragment_length,
        require_shift=require_uppercase,
    )

    if require_uppercase and not contains_shift_input(fragment):
        fragment = transform_random_shift(fragment)

    display_text = compose_password_text(fragment)

    actual_password = convert_to_dubeolsik(display_text)

    validation = validate_password(
        actual_password,
        min_length=min_password_length,
    )

    return GeneratedPassword(
        display_text=display_text,
        actual_password=actual_password,
        validation=validation,
    )
