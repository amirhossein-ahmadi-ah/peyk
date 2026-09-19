from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PaidMediaPreview:
    """The paid media isn't available before the payment.

Attributes:
    type: Type of the paid media, always 'preview'
    width: Media width as defined by the sender
    height: Media height as defined by the sender
    duration: Duration of the media in seconds as defined by the sender"""
    type: str = 'preview'
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PaidMediaPreview']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PaidMediaPreview']``).\n        "
        if data is None:
            return None
        return cls(type=_parse_api_value('String', data.get('type')), width=_parse_api_value('Integer', data.get('width')), height=_parse_api_value('Integer', data.get('height')), duration=_parse_api_value('Integer', data.get('duration')))
