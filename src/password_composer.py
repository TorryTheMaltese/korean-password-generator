import secrets

DEFAULT_MIN_DIGITS = 2
DEFAULT_MAX_DIGITS = 4

DEFAULT_MIN_SYMBOLS = 1
DEFAULT_MAX_SYMBOLS = 2

DEFAULT_SYMBOLS = "!@#$%^&*"


def generate_digits(
    min_count: int = DEFAULT_MIN_DIGITS,
    max_count: int = DEFAULT_MAX_DIGITS,
) -> str:
    """
    지정된 범위의 길이로 숫자 문자열을 생성한다.
    """

    if min_count < 1:
        raise ValueError("숫자 최소 개수는 1 이상이어야 합니다.")

    if max_count < min_count:
        raise ValueError("숫자 최대 개수는 최소 개수보다 " "크거나 같아야 합니다.")

    count = min_count + secrets.randbelow(max_count - min_count + 1)

    return "".join(secrets.choice("0123456789") for _ in range(count))


def generate_symbols(
    allowed_symbols: str = DEFAULT_SYMBOLS,
    min_count: int = DEFAULT_MIN_SYMBOLS,
    max_count: int = DEFAULT_MAX_SYMBOLS,
) -> str:
    """
    허용된 특수문자 목록에서 무작위 문자열을 생성한다.
    """

    if not allowed_symbols:
        raise ValueError("사용 가능한 특수문자가 없습니다.")

    if min_count < 1:
        raise ValueError("특수문자 최소 개수는 1 이상이어야 합니다.")

    if max_count < min_count:
        raise ValueError("특수문자 최대 개수는 최소 개수보다 " "크거나 같아야 합니다.")

    count = min_count + secrets.randbelow(max_count - min_count + 1)

    return "".join(secrets.choice(allowed_symbols) for _ in range(count))


def compose_password_text(
    hangul_text: str,
    *,
    min_digits: int = DEFAULT_MIN_DIGITS,
    max_digits: int = DEFAULT_MAX_DIGITS,
    min_symbols: int = DEFAULT_MIN_SYMBOLS,
    max_symbols: int = DEFAULT_MAX_SYMBOLS,
    allowed_symbols: str = DEFAULT_SYMBOLS,
) -> str:
    """
    기억용 한글 문자열에 숫자와 특수문자를 조합한다.

    기본 형식:
        한글 + 숫자 + 특수문자

    예:
        까마득
        → 까마득34##
    """

    if not hangul_text:
        raise ValueError("한글 문자열이 비어 있습니다.")

    digits = generate_digits(
        min_digits,
        max_digits,
    )

    symbols = generate_symbols(
        allowed_symbols,
        min_symbols,
        max_symbols,
    )

    return hangul_text + digits + symbols
