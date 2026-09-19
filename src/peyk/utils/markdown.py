"""Telegram MarkdownV2 syntax helpers; these strings are not portable across platforms."""
from __future__ import annotations

_SPECIAL = r"_[]()~`>#+-=|{}.!"


def escape(value: str) -> str:
    """Escape Telegram MarkdownV2 text."""
    return "".join("\\" + ch if ch in _SPECIAL else ch for ch in value)


def bold(value: str) -> str:
    """Wrap ``value`` in Telegram MarkdownV2 bold markup."""
    return f"*{escape(value)}*"


def italic(value: str) -> str:
    """Wrap ``value`` in Telegram MarkdownV2 italic markup."""
    return f"_{escape(value)}_"


def underline(value: str) -> str:
    """Wrap ``value`` in Telegram MarkdownV2 underline markup."""
    return f"__{escape(value)}__"


def strikethrough(value: str) -> str:
    """Wrap ``value`` in Telegram MarkdownV2 strikethrough markup."""
    return f"~{escape(value)}~"


def spoiler(value: str) -> str:
    """Wrap ``value`` in Telegram MarkdownV2 spoiler markup."""
    return f"||{escape(value)}||"


def code(value: str) -> str:
    """Wrap ``value`` in Telegram MarkdownV2 inline code."""
    return "`" + value.replace("`", "\\`") + "`"


def pre(value: str, language: str | None = None) -> str:
    """Wrap ``value`` in Telegram MarkdownV2 preformatted markup."""
    return "```" + (language or "") + "\\n" + value.replace("`", "\\`") + "\\n```"

def link(value: str, url: str) -> str:
    """Create a Telegram MarkdownV2 link."""
    safe_url = url.replace("\\", "\\\\").replace(")", "\\)")
    return f"[{escape(value)}]({safe_url})"


def text_mention(value: str, user_id: int | str) -> str:
    """Create a Telegram MarkdownV2 user mention."""
    return link(value, f"tg://user?id={user_id}")


def quote(value: str, expandable: bool = False) -> str:
    """Create a Telegram MarkdownV2 block quote."""
    lines = value.splitlines() or [""]
    prefix = ">" if not expandable else "> "
    return "\n".join(f"{prefix}{escape(line)}" for line in lines)


def blockquote(value: str) -> str:
    """Alias for :func:`quote`, matching aiogram's helper naming."""
    return quote(value)


def expandable_blockquote(value: str) -> str:
    """Create an expandable Telegram block quote."""
    return quote(value, expandable=True)


__all__ = ["escape", "bold", "italic", "underline", "strikethrough", "spoiler", "code", "pre", "link", "text_mention", "quote", "blockquote", "expandable_blockquote"]
