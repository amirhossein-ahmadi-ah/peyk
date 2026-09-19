from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputPaidMediaPhoto:
    """The paid media to send is a photo.

Attributes:
    type: Type of the media, must be photo
    media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files"""
    media: str
    type: str = 'photo'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InputPaidMediaPhoto']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InputPaidMediaPhoto']``).\n        "
        if data is None:
            return None
        return cls(media=_parse_api_value('String', data.get('media')), type=_parse_api_value('String', data.get('type')))
