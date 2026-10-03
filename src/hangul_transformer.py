def get_shift_transformations(char: str) -> list[str]:
    """
    한 글자에서 만들 수 있는 Shift 입력 형태를 모두 반환한다.

    초성과 중성이 각각 Shift 형태로 변환 가능한 경우,
    개별 변환뿐 아니라 동시 변환도 후보에 포함한다.

    예:
        가 → ["까"]

        개 →
            "깨"  (초성만: ㄱ → ㄲ)
            "걔"  (중성만: ㅐ → ㅒ)
            "꺠"  (초성 + 중성)

        배 →
            "빼"  (초성만: ㅂ → ㅃ)
            "뱨"  (중성만: ㅐ → ㅒ)
            "뺴"  (초성 + 중성)

    종성은 항상 그대로 유지한다.
    """

    if not is_hangul_syllable(char):
        return []

    initial_index, medial_index, final_index = (
        decompose_syllable(char)
    )

    transformations = []

    shifted_initial = SHIFT_INITIAL_MAP.get(
        initial_index
    )

    shifted_medial = SHIFT_MEDIAL_MAP.get(
        medial_index
    )

    # 1. 초성만 Shift 형태로 변환
    if shifted_initial is not None:
        transformations.append(
            compose_syllable(
                shifted_initial,
                medial_index,
                final_index,
            )
        )

    # 2. 중성만 Shift 형태로 변환
    if shifted_medial is not None:
        transformations.append(
            compose_syllable(
                initial_index,
                shifted_medial,
                final_index,
            )
        )

    # 3. 초성과 중성을 모두 Shift 형태로 변환
    if (
        shifted_initial is not None
        and shifted_medial is not None
    ):
        transformations.append(
            compose_syllable(
                shifted_initial,
                shifted_medial,
                final_index,
            )
        )

    return transformations