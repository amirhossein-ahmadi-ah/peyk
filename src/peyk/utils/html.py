"""Telegram HTML syntax helpers; these strings are not portable across platforms."""
from __future__ import annotations

from html import escape


def bold(value: str) -> str:
    """Wrap ``value`` in Telegram HTML bold markup."""
    return f"<b>{escape(value, quote=False)}</b>"


def italic(value: str) -> str:
    """Wrap ``value`` in Telegram HTML italic markup."""
    return f"<i>{escape(value, quote=False)}</i>"


def underline(value: str) -> str:
    """Wrap ``value`` in Telegram HTML underline markup."""
    return f"<u>{escape(value, quote=False)}</u>"


def strikethrough(value: str) -> str:
    """Wrap ``value`` in Telegram HTML strikethrough markup."""
    return f"<s>{escape(value, quote=False)}</s>"


def spoiler(value: str) -> str:
    """Wrap ``value`` in Telegram HTML spoiler markup."""
    return f"<tg-spoiler>{escape(value, quote=False)}</tg-spoiler>"


def code(value: str) -> str:
    """Wrap ``value`` in Telegram HTML inline-code markup."""
    return f"<code>{escape(value, quote=False)}</code>"


def pre(value: str, language: str | None = None) -> str:
    """Wrap ``value`` in Telegram HTML preformatted markup."""
    body = escape(value, quote=False)
    if language is None:
        return f"<pre>{body}</pre>"
    return f'<pre><code class="language-{escape(language, quote=True)}">{body}</code></pre>'


def link(value: str, url: str) -> str:
    """Wrap ``value`` in a Telegram HTML link."""
    return f'<a href="{escape(url, quote=True)}">{escape(value, quote=False)}</a>'


def text_mention(value: str, user_id: int | str) -> str:
    """Create a Telegram HTML user mention."""
    return link(value, f"tg://user?id={user_id}")


def mention(value: str, user_id: int | str) -> str:
    """Create a Telegram HTML user mention."""
    return text_mention(value, user_id)


def quote(value: str, expandable: bool = False) -> str:
    """Wrap ``value`` in Telegram HTML blockquote markup."""
    attribute = " expandable" if expandable else ""
    return f"<blockquote{attribute}>{escape(value, quote=False)}</blockquote>"


def blockquote(value: str) -> str:
    """Alias for :func:`quote`, matching aiogram's helper naming."""
    return quote(value)


def expandable_blockquote(value: str) -> str:
    """Create an expandable Telegram block quote."""
    return quote(value, expandable=True)


__all__ = ["bold", "italic", "underline", "strikethrough", "spoiler", "code", "pre", "link", "text_mention", "mention", "quote", "blockquote", "expandable_blockquote"]
