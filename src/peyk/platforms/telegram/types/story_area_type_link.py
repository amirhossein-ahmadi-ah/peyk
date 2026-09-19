from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StoryAreaTypeLink:
    """Describes a story area pointing to an HTTP or tg:// link. Currently, a story can have up to 3 link areas.

Attributes:
    type: Type of the area, always 'link'
    url: HTTP or tg:// URL to be opened when the area is clicked"""
    url: str
    type: str = 'link'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StoryAreaTypeLink']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StoryAreaTypeLink']``).\n        "
        if data is None:
            return None
        return cls(url=_parse_api_value('String', data.get('url')), type=_parse_api_value('String', data.get('type')))
