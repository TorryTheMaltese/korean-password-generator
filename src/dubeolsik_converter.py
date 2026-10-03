from hangul_transformer import (
    HANGUL_BASE,
    HANGUL_END,
    decompose_syllable,
)


# 초성 → 두벌식 영문 키
INITIAL_KEYS = [
    "r",   # ㄱ
    "R",   # ㄲ
    "s",   # ㄴ
    "e",   # ㄷ
    "E",   # ㄸ
    "f",   # ㄹ
    "a",   # ㅁ
    "q",   # ㅂ
    "Q",   # ㅃ
    "t",   # ㅅ
    "T",   # ㅆ
    "d",   # ㅇ
    "w",   # ㅈ
    "W",   # ㅉ
    "c",   # ㅊ
    "z",   # ㅋ
    "x",   # ㅌ
    "v",   # ㅍ
    "g",   # ㅎ
]


# 중성 → 두벌식 영문 키
#
# 복합 모음은 실제 입력하는 키 순서를 그대로 표현한다.
MEDIAL_KEYS = [
    "k",    # ㅏ
    "o",    # ㅐ
    "i",    # ㅑ
    "O",    # ㅒ
    "j",    # ㅓ
    "p",    # ㅔ
    "u",    # ㅕ
    "P",    # ㅖ
    "h",    # ㅗ
    "hk",   # ㅘ
    "ho",   # ㅙ
    "hl",   # ㅚ
    "y",    # ㅛ
    "n",    # ㅜ
    "nj",   # ㅝ
    "np",   # ㅞ
    "nl",   # ㅟ
    "b",    # ㅠ
    "m",    # ㅡ
    "ml",   # ㅢ
    "l",    # ㅣ
]


# 종성 → 두벌식 영문 키
#
# 0번은 종성이 없는 경우.
# 겹받침은 실제 입력하는 키 순서를 그대로 표현한다.
FINAL_KEYS = [
    "",     # 없음
    "r",    # ㄱ
    "R",    # ㄲ
    "rt",   # ㄳ
    "s",    # ㄴ
    "sw",   # ㄵ
    "sg",   # ㄶ
    "e",    # ㄷ
    "f",    # ㄹ
    "fr",   # ㄺ
    "fa",   # ㄻ
    "fq",   # ㄼ
    "ft",   # ㄽ
    "fx",   # ㄾ
    "fv",   # ㄿ
    "fg",   # ㅀ
    "a",    # ㅁ
    "q",    # ㅂ
    "qt",   # ㅄ
    "t",    # ㅅ
    "T",    # ㅆ
    "d",    # ㅇ
    "w",    # ㅈ
    "c",    # ㅊ
    "z",    # ㅋ
    "x",    # ㅌ
    "v",    # ㅍ
    "g",    # ㅎ
]


def is_hangul_syllable(char: str) -> bool:
    """
    문자가 완성형 한글 음절인지 확인한다.
    """

    return (
        len(char) == 1
        and HANGUL_BASE <= ord(char) <= HANGUL_END
    )


def convert_syllable_to_keys(char: str) -> str:
    """
    완성형 한글 음절 하나를 실제 두벌식 영문 키 입력으로 변환한다.

    예:
        가 → rk
        까 → Rk
        예 → dP
        뺴 → QO
        과 → rhk
        읽 → dlfr

    Raises:
        ValueError:
            완성형 한글 음절이 아닌 경우.
    """

    if not is_hangul_syllable(char):
        raise ValueError(
            f"완성형 한글 음절이 아닙니다: {char}"
        )

    initial_index, medial_index, final_index = (
        decompose_syllable(char)
    )

    return (
        INITIAL_KEYS[initial_index]
        + MEDIAL_KEYS[medial_index]
        + FINAL_KEYS[final_index]
    )


def convert_to_dubeolsik(text: str) -> str:
    """
    한글 기억 문자열을 실제 두벌식 영문 키 입력 문자열로 변환한다.

    완성형 한글은 두벌식 키 입력으로 변환하고,
    영문·숫자·특수문자는 그대로 유지한다.

    이 함수의 반환값은 사용자에게 표시하기 위한 값이 아니라
    비밀번호 복잡도 등을 내부적으로 검증하기 위한 값이다.

    예:
        까마득34##
        → Rkakemr34##
    """

    converted = []

    for char in text:
        if is_hangul_syllable(char):
            converted.append(
                convert_syllable_to_keys(char)
            )
        else:
            converted.append(char)

    return "".join(converted)
