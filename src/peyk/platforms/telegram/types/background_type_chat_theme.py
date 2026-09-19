from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BackgroundTypeChatTheme:
    """The background is taken directly from a built-in chat theme.

Attributes:
    type: Type of the background, always 'chat_theme'
    theme_name: Name of the chat theme, which is usually an emoji"""
    type: str = 'chat_theme'
    theme_name: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BackgroundTypeChatTheme']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BackgroundTypeChatTheme']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'chat_theme'), theme_name=data.get('theme_name', ''))
