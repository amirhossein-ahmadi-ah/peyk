from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .web_app_info import WebAppInfo
@dataclass
class KeyboardButton:
    """One button of the reply keyboard.

    Attributes:
        text: Text of the button.
        request_contact: If True, the user's phone number is requested.
        request_location: If True, the user's current location is requested.
        web_app: Description of the Web App launched when button is pressed.
        style: Button color style: 'primary' (blue), 'success' (green), 'danger' (red).
    """
    text: str
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    web_app: Optional[WebAppInfo] = None
    style: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['KeyboardButton']:
        """Parse raw Bale data into ``KeyboardButton``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[KeyboardButton]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(
            text=data.get('text', ''),
            request_contact=data.get('request_contact'),
            request_location=data.get('request_location'),
            web_app=WebAppInfo.from_dict(data.get('web_app')),
            style=data.get('style'),
        )
