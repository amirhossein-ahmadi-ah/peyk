from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ForumTopicEdited:
    """This object represents a service message about an edited forum topic.

Attributes:
    name: New name of the topic, if it was edited
    icon_custom_emoji_id: New identifier of the custom emoji shown as the topic icon, if it was edited; an empty string if the icon was removed"""
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ForumTopicEdited']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ForumTopicEdited']``).\n        "
        if data is None:
            return None
        return cls(name=data.get('name'), icon_custom_emoji_id=data.get('icon_custom_emoji_id'))
