from phrase_loader import load_phrases
from phrase_selector import select_random_fragment


def main() -> None:
    try:
        phrases = load_phrases()

        print(f"문구 {len(phrases)}개를 불러왔습니다.")

        fragment = select_random_fragment(phrases)

        # 개발 중 동작 확인용 출력.
        # 최종 프로그램에서는 출력 방식과 보안 정책을 별도로 정리할 예정.
        print(f"추출 문자열: {fragment}")

    except (FileNotFoundError, ValueError) as error:
        print(f"[오류] {error}")


if __name__ == "__main__":
    main()