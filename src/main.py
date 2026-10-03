from phrase_loader import load_phrases
from phrase_selector import select_random_fragment
from hangul_transformer import (
    contains_shift_candidate,
    contains_shift_input,
    transform_random_shift,
)


def main() -> None:
    try:
        phrases = load_phrases()

        print(
            f"문구 {len(phrases)}개를 불러왔습니다."
        )

        fragment = select_random_fragment(phrases)

        print(f"추출 문자열: {fragment}")

        if contains_shift_input(fragment):
            print(
                "Shift 변형: 이미 대문자 입력 요소가 "
                "포함되어 있습니다."
            )
            print(f"최종 문자열: {fragment}")

        elif contains_shift_candidate(fragment):
            transformed = transform_random_shift(
                fragment
            )

            print(f"Shift 변형: {transformed}")
            print(f"최종 문자열: {transformed}")

        else:
            print(
                "Shift 변형: 현재 추출 문자열에는 "
                "대문자 입력 요소를 만들 수 있는 "
                "글자가 없습니다."
            )

    except (FileNotFoundError, ValueError) as error:
        print(f"[오류] {error}")


if __name__ == "__main__":
    main()