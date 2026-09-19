"""Telegram ParseMode string-domain enum."""

from enum import StrEnum


class ParseMode(StrEnum):
    """Telegram Bot API parse-mode values."""

    MARKDOWN = "Markdown"
    MARKDOWN_V2 = "MarkdownV2"
    HTML = "HTML"
