from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichMessageMedia:
    """Describes a media element embedded in an outgoing rich message.

Attributes:
    id: Unique identifier of the media used in a tg://photo?id=, tg://video?id=, or tg://audio?id= link. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.
    media: The media to be sent. Everything except the media itself and its properties is ignored."""
    media: object = None
    type: Optional[str] = None

    def to_dict(self, media_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            media_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'media': media_ref}
        if self.type is not None:
            body['type'] = self.type
        return body
