import json
from pathlib import Path

from app_paths import (
    get_default_phrase_file,
    get_settings_file,
)


def load_last_phrase_file() -> Path:

    settings_file = get_settings_file()

    if not settings_file.exists():
        return get_default_phrase_file()

    try:
        with settings_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            settings = json.load(file)

        phrase_file = settings.get("phrase_file")

        if not phrase_file:
            return get_default_phrase_file()

        path = Path(phrase_file)

        if path.is_file():
            return path

    except (
        OSError,
        json.JSONDecodeError,
        TypeError,
    ):
        pass

    return get_default_phrase_file()


def save_last_phrase_file(
    file_path: str | Path,
) -> None:

    path = Path(file_path).resolve()

    if not path.is_file():
        raise ValueError(f"저장할 원본 문구 파일을 찾을 수 없습니다: {path}")

    settings_file = get_settings_file()

    settings_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings = {
        "phrase_file": str(path),
    }

    with settings_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            settings,
            file,
            ensure_ascii=False,
            indent=2,
        )
