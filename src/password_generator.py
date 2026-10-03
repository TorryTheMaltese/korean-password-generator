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
        기본 비밀번호 복잡도 검증 결과.
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
    include_digits: bool = True,
    min_digits: int = 2,
    max_digits: int = 4,
    include_symbols: bool = True,
    min_symbols: int = 1,
    max_symbols: int = 2,
    allowed_symbols: str = "!@#$%^&*",
) -> GeneratedPassword:
    """
    최종 비밀번호 후보를 생성하고 검증함.

    전달받은 설정에 따라 한글 문자열,
    Shift 변형, 숫자 및 특수문자를 조합함.
    """

    if min_fragment_length < 1:
        raise ValueError("추출 문자열의 최소 길이는 1 이상이어야 합니다.")

    if max_fragment_length < min_fragment_length:
        raise ValueError(
            "추출 문자열의 최대 길이는 " "최소 길이보다 크거나 같아야 합니다."
        )

    if include_digits:
        if min_digits < 1:
            raise ValueError("숫자 최소 개수는 1 이상이어야 합니다.")

        if max_digits < min_digits:
            raise ValueError("숫자 최대 개수는 " "최소 개수보다 크거나 같아야 합니다.")

    if include_symbols:
        if not allowed_symbols:
            raise ValueError("사용 가능한 특수문자를 하나 이상 입력해야 합니다.")

        if min_symbols < 1:
            raise ValueError("특수문자 최소 개수는 1 이상이어야 합니다.")

        if max_symbols < min_symbols:
            raise ValueError(
                "특수문자 최대 개수는 " "최소 개수보다 크거나 같아야 합니다."
            )

    fragment = select_random_fragment(
        phrases,
        min_length=min_fragment_length,
        max_length=max_fragment_length,
        require_shift=require_uppercase,
    )

    if require_uppercase and not contains_shift_input(fragment):
        fragment = transform_random_shift(fragment)

    display_text = compose_password_text(
        fragment,
        include_digits=include_digits,
        min_digits=min_digits,
        max_digits=max_digits,
        include_symbols=include_symbols,
        min_symbols=min_symbols,
        max_symbols=max_symbols,
        allowed_symbols=allowed_symbols,
    )

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
