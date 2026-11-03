from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .copy_text_button import CopyTextButton
from .web_app_info import WebAppInfo
@dataclass
class InlineKeyboardButton:
    """One button of an inline keyboard.

    Attributes:
        text: Label text on the button.
        url: HTTP or ble.ir URL to open.
        callback_data: Data sent in a callback query to the bot (1-64 bytes).
        web_app: Description of the Web App launched when button is pressed.
        copy_text: Description of the button that copies text to clipboard.
        style: Button color style: 'primary' (blue), 'success' (green), 'danger' (red).
    """
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    copy_text: Optional[CopyTextButton] = None
    style: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InlineKeyboardButton']:
        """Parse raw Bale data into ``InlineKeyboardButton``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[InlineKeyboardButton]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(
            text=data.get('text', ''),
            url=data.get('url'),
            callback_data=data.get('callback_data'),
            web_app=WebAppInfo.from_dict(data.get('web_app')),
            copy_text=CopyTextButton.from_dict(data.get('copy_text')),
            style=data.get('style'),
        )
