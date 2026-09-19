"""Telegram PassportElementErrorSource string-domain enum."""

from enum import StrEnum


class PassportElementErrorSource(StrEnum):
    """Telegram Passport element-error source values."""

    DATA = "data"
    FRONT_SIDE = "front_side"
    REVERSE_SIDE = "reverse_side"
    SELFIE = "selfie"
    FILE = "file"
    FILES = "files"
    TRANSLATION_FILE = "translation_file"
    TRANSLATION_FILES = "translation_files"
    UNSPECIFIED = "unspecified"
