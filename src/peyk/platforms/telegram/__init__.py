"""Telegram platform adapter and compatibility exports."""

from .client import TelegramClient, build_inline_keyboard_button
from .errors import ResponseParameters, TelegramAPIError
from .models import *  # noqa: F401,F403
from .enums import *  # noqa: F401,F403

__all__ = sorted({
    "TelegramClient",
    "build_inline_keyboard_button",
    "ResponseParameters",
    "TelegramAPIError",
    *[name for name in globals() if not name.startswith("_")],
})
