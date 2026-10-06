import os
import sys
from pathlib import Path

APP_NAME = "KoreanPasswordGenerator"


def get_app_directory() -> Path:

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent


def get_default_phrase_file() -> Path:
    return get_app_directory() / "phrases.txt"


def get_settings_directory() -> Path:
    appdata = os.getenv("APPDATA")

    if appdata:
        return Path(appdata) / APP_NAME

    return Path.home() / f".{APP_NAME}"


def get_settings_file() -> Path:
    return get_settings_directory() / "settings.json"
