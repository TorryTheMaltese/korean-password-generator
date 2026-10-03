from dataclasses import dataclass

DEFAULT_MIN_LENGTH = 8


@dataclass(frozen=True)
class ValidationResult:
    """
    비밀번호 복잡도 검증 결과.
    """

    is_valid: bool
    length: int

    has_uppercase: bool
    has_lowercase: bool
    has_digit: bool
    has_special: bool

    errors: tuple[str, ...]


def validate_password(
    password: str,
    min_length: int = DEFAULT_MIN_LENGTH,
) -> ValidationResult:
    """
    실제 두벌식 키 입력 결과를 기준으로
    비밀번호 복잡도를 검증한다.

    기본 조건:
        - 최소 8자 이상
        - 영문 대문자 1개 이상
        - 영문 소문자 1개 이상
        - 숫자 1개 이상
        - 특수문자 1개 이상

    Args:
        password:
            한글 기억 문자열이 아닌,
            두벌식 영문 키 입력으로 변환된 실제 비밀번호.

        min_length:
            최소 비밀번호 길이.

    Returns:
        ValidationResult
    """

    if min_length < 1:
        raise ValueError("최소 비밀번호 길이는 1 이상이어야 합니다.")

    has_uppercase = any(char.isascii() and char.isupper() for char in password)

    has_lowercase = any(char.isascii() and char.islower() for char in password)

    has_digit = any(char.isascii() and char.isdigit() for char in password)

    has_special = any(
        char.isascii() and not char.isalnum() and not char.isspace()
        for char in password
    )

    errors = []

    if len(password) < min_length:
        errors.append(f"최소 {min_length}자 이상이어야 합니다.")

    if not has_uppercase:
        errors.append("영문 대문자가 1개 이상 필요합니다.")

    if not has_lowercase:
        errors.append("영문 소문자가 1개 이상 필요합니다.")

    if not has_digit:
        errors.append("숫자가 1개 이상 필요합니다.")

    if not has_special:
        errors.append("특수문자가 1개 이상 필요합니다.")

    return ValidationResult(
        is_valid=not errors,
        length=len(password),
        has_uppercase=has_uppercase,
        has_lowercase=has_lowercase,
        has_digit=has_digit,
        has_special=has_special,
        errors=tuple(errors),
    )
