from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PaidMediaVideo:
    """The paid media is a video.

Attributes:
    type: Type of the paid media, always 'video'
    video: The video"""
    video: Video
    type: str = 'video'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PaidMediaVideo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PaidMediaVideo']``).\n        "
        if data is None:
            return None
        return cls(video=_parse_api_value('Video', data.get('video')), type=_parse_api_value('String', data.get('type')))
