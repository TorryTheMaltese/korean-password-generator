from pathlib import Path


DEFAULT_PHRASE_FILE = Path("phrases.txt")


def load_phrases(file_path: str | Path = DEFAULT_PHRASE_FILE) -> list[str]:
    """
    텍스트 파일에서 비밀번호 생성에 사용할 원본 문구를 불러온다.

    - 빈 줄은 제외한다.
    - 각 줄의 앞뒤 공백은 제거한다.
    - 파일이 없거나 유효한 문구가 없으면 예외를 발생시킨다.

    Args:
        file_path:
            원본 문구가 저장된 텍스트 파일 경로.
            기본값은 프로젝트 루트의 'phrases.txt'.

    Returns:
        유효한 문구 문자열 목록.

    Raises:
        FileNotFoundError:
            지정한 파일이 존재하지 않는 경우.

        ValueError:
            파일은 존재하지만 유효한 문구가 하나도 없는 경우.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"원본 문구 파일을 찾을 수 없습니다: {path}\n"
            "phrases.example.txt를 복사하여 phrases.txt를 생성해주세요."
        )

    if not path.is_file():
        raise ValueError(f"지정한 경로가 파일이 아닙니다: {path}")

    with path.open("r", encoding="utf-8") as file:
        phrases = [
            line.strip()
            for line in file
            if line.strip()
        ]

    if not phrases:
        raise ValueError(
            f"파일에 사용할 수 있는 문구가 없습니다: {path}"
        )

    return phrases