import secrets

from hangul_transformer import contains_shift_candidate


DEFAULT_MIN_LENGTH = 3
DEFAULT_MAX_LENGTH = 5


def normalize_phrase(phrase: str) -> str:
    """
    원본 문구에서 완성형 한글 음절만 남긴다.
    """

    return "".join(
        char
        for char in phrase
        if "가" <= char <= "힣"
    )


def build_fragment_candidates(
    phrases: list[str],
    min_length: int = DEFAULT_MIN_LENGTH,
    max_length: int = DEFAULT_MAX_LENGTH,
    require_shift: bool = False,
) -> list[str]:
    """
    조건을 만족하는 모든 문자열 후보를 생성한다.

    require_shift=True인 경우,
    이미 Shift 입력 요소가 있거나 Shift 형태로
    변형 가능한 문자열만 후보에 포함한다.
    """

    if not phrases:
        raise ValueError(
            "원본 문구 목록이 비어 있습니다."
        )

    if min_length < 1:
        raise ValueError(
            "최소 길이는 1 이상이어야 합니다."
        )

    if max_length < min_length:
        raise ValueError(
            "최대 길이는 최소 길이보다 "
            "크거나 같아야 합니다."
        )

    candidates = []

    for phrase in phrases:
        normalized = normalize_phrase(phrase)

        if len(normalized) < min_length:
            continue

        actual_max_length = min(
            max_length,
            len(normalized),
        )

        for length in range(
            min_length,
            actual_max_length + 1,
        ):
            for start_index in range(
                len(normalized) - length + 1
            ):
                fragment = normalized[
                    start_index:start_index + length
                ]

                if (
                    require_shift
                    and not contains_shift_candidate(fragment)
                ):
                    continue

                candidates.append(fragment)

    return candidates


def select_random_fragment(
    phrases: list[str],
    min_length: int = DEFAULT_MIN_LENGTH,
    max_length: int = DEFAULT_MAX_LENGTH,
    require_shift: bool = False,
) -> str:
    """
    조건을 만족하는 문자열 후보 중 하나를
    secrets.choice()로 무작위 선택한다.
    """

    candidates = build_fragment_candidates(
        phrases=phrases,
        min_length=min_length,
        max_length=max_length,
        require_shift=require_shift,
    )

    if not candidates:
        if require_shift:
            raise ValueError(
                "Shift 입력 요소를 포함하거나 "
                "Shift 형태로 변형할 수 있는 "
                "문자열이 없습니다."
            )

        raise ValueError(
            "조건을 만족하는 한글 문자열이 없습니다."
        )

    return secrets.choice(candidates)