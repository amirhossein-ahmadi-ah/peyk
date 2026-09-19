from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ForumTopicCreated:
    """This object represents a service message about a new forum topic created in the chat.

Attributes:
    name: Name of the topic
    icon_color: Color of the topic icon in RGB format
    icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon
    is_name_implicit: True, if the name of the topic wasn't specified explicitly by its creator and likely needs to be changed by the bot"""
    name: str = ''
    icon_color: Optional[int] = None
    icon_custom_emoji_id: Optional[str] = None
    is_name_implicit: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ForumTopicCreated']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ForumTopicCreated']``).\n        "
        if data is None:
            return None
        return cls(name=data.get('name', ''), icon_color=data.get('icon_color'), icon_custom_emoji_id=data.get('icon_custom_emoji_id'), is_name_implicit=data.get('is_name_implicit'))
