from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class MetadataPart:
    """Represent the Rubika Bot API ``MetadataPart`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    type: str = ''
    from_index: int = 0
    length: int = 0
    link_url: Optional[str] = None
    mention_text_user_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MetadataPart']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MetadataPart']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', ''), from_index=_to_int(data.get('from_index')) or 0, length=_to_int(data.get('length')) or 0, link_url=data.get('link_url'), mention_text_user_id=_to_str(data.get('mention_text_user_id')))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'from_index': self.from_index, 'length': self.length}
        if self.link_url is not None:
            body['link_url'] = self.link_url
        if self.mention_text_user_id is not None:
            body['mention_text_user_id'] = self.mention_text_user_id
        return body
