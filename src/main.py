from phrase_loader import load_phrases
from password_generator import generate_password


def main() -> None:
    try:
        phrases = load_phrases()

        print(
            f"문구 {len(phrases)}개를 불러왔습니다."
        )

        result = generate_password(phrases)

        print()
        print(
            f"🔐 생성 문자열: "
            f"{result.display_text}"
        )

        # 개발 중 검증용.
        # 최종 GUI에서는 표시하지 않는다.
        print(
            f"[DEBUG] 실제 두벌식 입력: "
            f"{result.actual_password}"
        )

        print()
        print("[검증 결과]")
        print(
            f"길이: {result.validation.length}"
        )
        print(
            f"대문자: "
            f"{result.validation.has_uppercase}"
        )
        print(
            f"소문자: "
            f"{result.validation.has_lowercase}"
        )
        print(
            f"숫자: "
            f"{result.validation.has_digit}"
        )
        print(
            f"특수문자: "
            f"{result.validation.has_special}"
        )

        if result.validation.is_valid:
            print("결과: PASS")

        else:
            print("결과: FAIL")

            for error in result.validation.errors:
                print(f" - {error}")

    except (FileNotFoundError, ValueError) as error:
        print(f"[오류] {error}")


if __name__ == "__main__":
    main()