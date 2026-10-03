from phrase_loader import load_phrases


def main() -> None:
    try:
        phrases = load_phrases()

        print(f"문구 {len(phrases)}개를 불러왔습니다.")

        # 보안상 실제 프로그램에서는 문구 내용을 자동 출력하지 않을 예정.
        # 현재는 개발 중 동작 확인을 위해 개수만 출력한다.

    except (FileNotFoundError, ValueError) as error:
        print(f"[오류] {error}")


if __name__ == "__main__":
    main()