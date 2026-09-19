"""Telegram PollType string-domain enum."""

from enum import StrEnum


class PollType(StrEnum):
    """Telegram poll type values."""

    REGULAR = "regular"
    QUIZ = "quiz"
