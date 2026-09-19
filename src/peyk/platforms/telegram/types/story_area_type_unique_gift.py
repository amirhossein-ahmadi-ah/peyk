from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StoryAreaTypeUniqueGift:
    """Describes a story area pointing to a unique gift. Currently, a story can have at most 1 unique gift area.

Attributes:
    type: Type of the area, always 'unique_gift'
    name: Unique name of the gift"""
    type: str = 'unique_gift'
    name: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StoryAreaTypeUniqueGift']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StoryAreaTypeUniqueGift']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'unique_gift'), name=data.get('name', ''))
