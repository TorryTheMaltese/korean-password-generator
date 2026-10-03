import secrets

HANGUL_BASE = 0xAC00
HANGUL_END = 0xD7A3

INITIAL_COUNT = 19
MEDIAL_COUNT = 21
FINAL_COUNT = 28

SYLLABLES_PER_INITIAL = MEDIAL_COUNT * FINAL_COUNT


# 두벌식에서 Shift 입력이 필요한 초성
#
# 1  ㄲ
# 4  ㄸ
# 8  ㅃ
# 10 ㅆ
# 13 ㅉ
SHIFT_INITIALS = {
    1,
    4,
    8,
    10,
    13,
}


# 일반 초성 → Shift 초성
SHIFT_INITIAL_MAP = {
    0: 1,  # ㄱ → ㄲ
    3: 4,  # ㄷ → ㄸ
    7: 8,  # ㅂ → ㅃ
    9: 10,  # ㅅ → ㅆ
    12: 13,  # ㅈ → ㅉ
}


# 두벌식에서 Shift 입력이 필요한 중성
#
# 3  ㅒ
# 7  ㅖ
SHIFT_MEDIALS = {
    3,
    7,
}


# 일반 중성 → Shift 중성
SHIFT_MEDIAL_MAP = {
    1: 3,  # ㅐ → ㅒ
    5: 7,  # ㅔ → ㅖ
}


def is_hangul_syllable(char: str) -> bool:
    """
    문자가 완성형 한글 음절인지 확인한다.
    """

    return len(char) == 1 and HANGUL_BASE <= ord(char) <= HANGUL_END


def decompose_syllable(
    char: str,
) -> tuple[int, int, int]:
    """
    완성형 한글 음절을
    초성·중성·종성 인덱스로 분해한다.
    """

    if not is_hangul_syllable(char):
        raise ValueError(f"완성형 한글 음절이 아닙니다: {char}")

    syllable_index = ord(char) - HANGUL_BASE

    initial_index = syllable_index // SYLLABLES_PER_INITIAL

    medial_index = (syllable_index % SYLLABLES_PER_INITIAL) // FINAL_COUNT

    final_index = syllable_index % FINAL_COUNT

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
    초성·중성·종성 인덱스를
    완성형 한글 음절로 조립한다.
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
    해당 한글 음절에 두벌식 Shift 입력이
    필요한 자모가 포함되어 있는지 확인한다.

    대상:
        ㄲ, ㄸ, ㅃ, ㅆ, ㅉ, ㅒ, ㅖ
    """

    if not is_hangul_syllable(char):
        return False

    initial_index, medial_index, _ = decompose_syllable(char)

    return initial_index in SHIFT_INITIALS or medial_index in SHIFT_MEDIALS


def contains_shift_input(text: str) -> bool:
    """
    문자열에 Shift 입력이 필요한 한글 음절이
    하나 이상 포함되어 있는지 확인한다.
    """

    return any(has_shift_input(char) for char in text)


def can_transform_to_shift(char: str) -> bool:
    """
    한글 음절이 이미 Shift 자모를 포함하거나,
    Shift 형태로 변형 가능한지 확인한다.
    """

    if not is_hangul_syllable(char):
        return False

    initial_index, medial_index, _ = decompose_syllable(char)

    return (
        initial_index in SHIFT_INITIALS
        or medial_index in SHIFT_MEDIALS
        or initial_index in SHIFT_INITIAL_MAP
        or medial_index in SHIFT_MEDIAL_MAP
    )


def contains_shift_candidate(text: str) -> bool:
    """
    문자열에 Shift 입력 요소가 이미 존재하거나
    Shift 형태로 변형 가능한 글자가 있는지 확인한다.
    """

    return any(can_transform_to_shift(char) for char in text)


def get_shift_transformations(
    char: str,
) -> list[str]:
    """
    한 글자에서 만들 수 있는 Shift 변형을 모두 반환한다.

    초성과 중성이 모두 변환 가능한 경우
    각각의 변형과 동시 변형을 모두 후보로 만든다.

    예:
        가 → 까

        배 →
            빼  (초성)
            뱨  (중성)
            뺴  (초성 + 중성)
    """

    if not is_hangul_syllable(char):
        return []

    initial_index, medial_index, final_index = decompose_syllable(char)

    transformations = []

    shifted_initial = SHIFT_INITIAL_MAP.get(initial_index)

    shifted_medial = SHIFT_MEDIAL_MAP.get(medial_index)

    # 초성만 변환
    if shifted_initial is not None:
        transformations.append(
            compose_syllable(
                shifted_initial,
                medial_index,
                final_index,
            )
        )

    # 중성만 변환
    if shifted_medial is not None:
        transformations.append(
            compose_syllable(
                initial_index,
                shifted_medial,
                final_index,
            )
        )

    # 초성과 중성을 동시에 변환
    if shifted_initial is not None and shifted_medial is not None:
        transformations.append(
            compose_syllable(
                shifted_initial,
                shifted_medial,
                final_index,
            )
        )

    return transformations


def transform_random_shift(text: str) -> str:
    """
    문자열이 두벌식 입력 시 영문 대문자를
    생성할 수 있도록 Shift 변형한다.

    이미 Shift 입력 요소가 포함되어 있다면
    원본 문자열을 그대로 반환한다.

    그렇지 않으면 가능한 모든 변형 중 하나를
    secrets.choice()로 무작위 선택한다.
    """

    if not text:
        raise ValueError("변환할 문자열이 비어 있습니다.")

    if contains_shift_input(text):
        return text

    candidates: list[tuple[int, str]] = []

    for index, char in enumerate(text):
        transformations = get_shift_transformations(char)

        for transformed_char in transformations:
            candidates.append((index, transformed_char))

    if not candidates:
        raise ValueError(
            "Shift 입력이 필요한 형태로 " "변환할 수 있는 글자가 없습니다."
        )

    selected_index, transformed_char = secrets.choice(candidates)

    characters = list(text)

    characters[selected_index] = transformed_char

    return "".join(characters)
