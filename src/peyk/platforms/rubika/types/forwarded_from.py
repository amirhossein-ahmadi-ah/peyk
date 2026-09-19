from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ForwardedFrom:
    """Represent the Rubika Bot API ``ForwardedFrom`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    type_from: Optional[str] = None
    message_id: Optional[str] = None
    from_chat_id: Optional[str] = None
    from_sender_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ForwardedFrom']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ForwardedFrom']``).\n        "
        if data is None:
            return None
        return cls(type_from=data.get('type_from'), message_id=_to_str(data.get('message_id')), from_chat_id=_to_str(data.get('from_chat_id')), from_sender_id=_to_str(data.get('from_sender_id')))
