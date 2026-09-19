from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StoryArea:
    """Describes a clickable area on a story media.

Attributes:
    position: Position of the area
    type: Type of the area"""
    position: Optional[StoryAreaPosition] = None
    type: Optional[StoryAreaType] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StoryArea']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StoryArea']``).\n        "
        if data is None:
            return None
        return cls(position=StoryAreaPosition.from_dict(data.get('position')), type=parse_story_area_type(data.get('type')))
