from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ButtonSelectionItem:
    """Represent the Rubika Bot API ``ButtonSelectionItem`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    text: str = ''
    image_url: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ButtonSelectionItem']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ButtonSelectionItem']``).\n        "
        if data is None:
            return None
        return cls(text=data.get('text', ''), image_url=data.get('image_url'), type=data.get('type'))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'text': self.text}
        if self.image_url is not None:
            body['image_url'] = self.image_url
        if self.type is not None:
            body['type'] = self.type
        return body
