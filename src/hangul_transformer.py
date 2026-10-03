# src/hangul_transformer.py

import secrets


HANGUL_BASE = 0xAC00
HANGUL_END = 0xD7A3

INITIAL_COUNT = 19
MEDIAL_COUNT = 21
FINAL_COUNT = 28

SYLLABLES_PER_INITIAL = MEDIAL_COUNT * FINAL_COUNT


# 초성 인덱스
#
#  0 ㄱ   1 ㄲ   2 ㄴ   3 ㄷ   4 ㄸ
#  5 ㄹ   6 ㅁ   7 ㅂ   8 ㅃ   9 ㅅ
# 10 ㅆ  11 ㅇ  12 ㅈ  13 ㅉ  14 ㅊ
# 15 ㅋ  16 ㅌ  17 ㅍ  18 ㅎ

SHIFT_INITIALS = {
    1,   # ㄲ
    4,   # ㄸ
    8,   # ㅃ
    10,  # ㅆ
    13,  # ㅉ
}


# Shift 입력을 유도할 수 있는 초성 변환
SHIFT_INITIAL_MAP = {
    0: 1,    # ㄱ → ㄲ
    3: 4,    # ㄷ → ㄸ
    7: 8,    # ㅂ → ㅃ
    9: 10,   # ㅅ → ㅆ
    12: 13,  # ㅈ → ㅉ
}


# 중성 인덱스
#
#  0 ㅏ   1 ㅐ   2 ㅑ   3 ㅒ   4 ㅓ
#  5 ㅔ   6 ㅕ   7 ㅖ   8 ㅗ   9 ㅘ
# 10 ㅙ  11 ㅚ  12 ㅛ  13 ㅜ  14 ㅝ
# 15 ㅞ  16 ㅟ  17 ㅠ  18 ㅡ  19 ㅢ
# 20 ㅣ

SHIFT_MEDIALS = {
    3,  # ㅒ
    7,  # ㅖ
}


# Shift 입력을 유도할 수 있는 중성 변환
SHIFT_MEDIAL_MAP = {
    1: 3,  # ㅐ → ㅒ
    5: 7,  # ㅔ → ㅖ
}


def is_hangul_syllable(char: str) -> bool:
    """
    문자가 완성형 한글 음절인지 확인한다.
    """

    return (
        len(char) == 1
        and HANGUL_BASE <= ord(char) <= HANGUL_END
    )


def decompose_syllable(char: str) -> tuple[int, int, int]:
    """
    완성형 한글 음절을 초성·중성·종성 인덱스로 분해한다.

    Returns:
        (초성 인덱스, 중성 인덱스, 종성 인덱스)

    Raises:
        ValueError:
            완성형 한글 음절이 아닌 경우.
    """

    if not is_hangul_syllable(char):
        raise ValueError(
            f"완성형 한글 음절이 아닙니다: {char}"
        )

    syllable_index = ord(char) - HANGUL_BASE

    initial_index = (
        syllable_index // SYLLABLES_PER_INITIAL
    )

    medial_index = (
        syllable_index % SYLLABLES_PER_INITIAL
    ) // FINAL_COUNT

    final_index = (
        syllable_index % FINAL_COUNT
    )

    return (
        initial_index,
        medial_index,
        final_index,
    )


def compose_syllable(
    initial_index: int,
    medial_index: int,
    final_index: int,
) -> str:
    """
    초성·중성·종성 인덱스를 완성형 한글 음절로 조립한다.
    """

    if not 0 <= initial_index < INITIAL_COUNT:
        raise ValueError("잘못된 초성 인덱스입니다.")

    if not 0 <= medial_index < MEDIAL_COUNT:
        raise ValueError("잘못된 중성 인덱스입니다.")

    if not 0 <= final_index < FINAL_COUNT:
        raise ValueError("잘못된 종성 인덱스입니다.")

    codepoint = (
        HANGUL_BASE
        + initial_index * SYLLABLES_PER_INITIAL
        + medial_index * FINAL_COUNT
        + final_index
    )

    return chr(codepoint)


def has_shift_input(char: str) -> bool:
    """
    해당 한글 음절을 두벌식으로 입력할 때
    Shift가 필요한 자모가 포함되어 있는지 확인한다.

    Shift 입력 대상:
        ㄲ, ㄸ, ㅃ, ㅆ, ㅉ, ㅒ, ㅖ
    """

    if not is_hangul_syllable(char):
        return False

    initial_index, medial_index, _ = (
        decompose_syllable(char)
    )

    return (
        initial_index in SHIFT_INITIALS
        or medial_index in SHIFT_MEDIALS
    )


def contains_shift_input(text: str) -> bool:
    """
    문자열에 두벌식 Shift 입력이 필요한 한글 음절이
    하나 이상 포함되어 있는지 확인한다.
    """

    return any(
        has_shift_input(char)
        for char in text
    )


def can_transform_to_shift(char: str) -> bool:
    """
    한글 음절을 Shift 입력이 필요한 형태로
    변형할 수 있는지 확인한다.

    이미 Shift 자모가 포함된 경우에도 True를 반환한다.
    """

    if not is_hangul_syllable(char):
        return False

    initial_index, medial_index, _ = (
        decompose_syllable(char)
    )

    return (
        initial_index in SHIFT_INITIALS
        or medial_index in SHIFT_MEDIALS
        or initial_index in SHIFT_INITIAL_MAP
        or medial_index in SHIFT_MEDIAL_MAP
    )


def contains_shift_candidate(text: str) -> bool:
    """
    문자열에 이미 Shift 자모가 있거나,
    Shift 입력 형태로 변형 가능한 글자가 있는지 확인한다.
    """

    return any(
        can_transform_to_shift(char)
        for char in text
    )


def get_shift_transformations(char: str) -> list[str]:
    """
    한 글자에서 만들 수 있는 Shift 입력 형태를 모두 반환한다.

    예:
        가 → ["까"]
        배 → ["빼", "뱨"]
        세 → ["쎄", "셰"]

    초성과 중성을 동시에 바꾸지는 않는다.
    가능한 변형 중 하나를 이후 secrets로 선택한다.
    """

    if not is_hangul_syllable(char):
        return []

    initial_index, medial_index, final_index = (
        decompose_syllable(char)
    )

    transformations = []

    if initial_index in SHIFT_INITIAL_MAP:
        transformations.append(
            compose_syllable(
                SHIFT_INITIAL_MAP[initial_index],
                medial_index,
                final_index,
            )
        )

    if medial_index in SHIFT_MEDIAL_MAP:
        transformations.append(
            compose_syllable(
                initial_index,
                SHIFT_MEDIAL_MAP[medial_index],
                final_index,
            )
        )

    return transformations


def transform_random_shift(text: str) -> str:
    """
    문자열이 두벌식 입력 시 영문 대문자를 만들 수 있도록 한다.

    이미 Shift 입력이 필요한 자모가 포함되어 있다면
    원본 문자열을 그대로 반환한다.

    그렇지 않으면 Shift 형태로 변형 가능한 모든 후보를
    수집하고, secrets를 이용해 하나를 무작위 선택한다.

    Args:
        text:
            변환할 한글 문자열.

    Returns:
        Shift 입력이 필요한 자모가 최소 하나 포함된 문자열.

    Raises:
        ValueError:
            빈 문자열이거나,
            Shift 형태로 변형 가능한 글자가 없는 경우.
    """

    if not text:
        raise ValueError(
            "변환할 문자열이 비어 있습니다."
        )

    # 원래 문구 자체에 ㄲ·ㄸ·ㅃ·ㅆ·ㅉ·ㅒ·ㅖ가 있다면
    # 이미 영문 대문자가 만들어지므로 변형할 필요가 없다.
    if contains_shift_input(text):
        return text

    candidates: list[tuple[int, str]] = []

    for index, char in enumerate(text):
        transformations = get_shift_transformations(char)

        for transformed_char in transformations:
            candidates.append(
                (index, transformed_char)
            )

    if not candidates:
        raise ValueError(
            "Shift 입력이 필요한 형태로 "
            "변환할 수 있는 글자가 없습니다."
        )

    selected_index, transformed_char = (
        secrets.choice(candidates)
    )

    characters = list(text)
    characters[selected_index] = transformed_char

    return "".join(characters)