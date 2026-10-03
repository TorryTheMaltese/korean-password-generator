# src/phrase_selector.py

import secrets


DEFAULT_MIN_LENGTH = 3
DEFAULT_MAX_LENGTH = 5


def normalize_phrase(phrase: str) -> str:
    """
    문자열 추출에 사용할 수 있도록 원본 문구를 정리한다.

    현재는 한글 음절만 남기고 공백, 숫자, 영문자,
    문장부호 등은 제거한다.

    Args:
        phrase:
            원본 문구.

    Returns:
        한글 완성형 음절만 남긴 문자열.
    """

    return "".join(
        char
        for char in phrase
        if "가" <= char <= "힣"
    )


def select_random_fragment(
    phrases: list[str],
    min_length: int = DEFAULT_MIN_LENGTH,
    max_length: int = DEFAULT_MAX_LENGTH,
) -> str:
    """
    원본 문구 목록에서 한글 문자열을 암호학적으로 안전하게 무작위 추출한다.

    1. 유효한 한글 문구만 후보로 선별한다.
    2. 후보 문구 중 하나를 secrets.choice()로 선택한다.
    3. min_length ~ max_length 범위에서 추출 길이를 무작위 결정한다.
    4. 선택한 문구에서 해당 길이의 연속 문자열을 무작위 추출한다.

    Args:
        phrases:
            원본 문구 문자열 목록.

        min_length:
            추출할 문자열의 최소 길이.

        max_length:
            추출할 문자열의 최대 길이.

    Returns:
        무작위로 선택된 한글 문자열.

    Raises:
        ValueError:
            문구 목록이 비어 있거나,
            길이 설정이 잘못되었거나,
            추출 가능한 문구가 없는 경우.
    """

    if not phrases:
        raise ValueError("원본 문구 목록이 비어 있습니다.")

    if min_length < 1:
        raise ValueError("최소 길이는 1 이상이어야 합니다.")

    if max_length < min_length:
        raise ValueError(
            "최대 길이는 최소 길이보다 크거나 같아야 합니다."
        )

    normalized_phrases = [
        normalize_phrase(phrase)
        for phrase in phrases
    ]

    valid_phrases = [
        phrase
        for phrase in normalized_phrases
        if len(phrase) >= min_length
    ]

    if not valid_phrases:
        raise ValueError(
            f"{min_length}글자 이상인 유효한 한글 문구가 없습니다."
        )

    phrase = secrets.choice(valid_phrases)

    actual_max_length = min(
        max_length,
        len(phrase),
    )

    fragment_length = (
        min_length
        + secrets.randbelow(actual_max_length - min_length + 1)
    )

    max_start_index = len(phrase) - fragment_length

    start_index = secrets.randbelow(
        max_start_index + 1
    )

    return phrase[
        start_index:start_index + fragment_length
    ]