from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Chat:
    """Represent the Rubika Bot API ``Chat`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    chat_id: str = ''
    chat_type: str = ''
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Chat']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Chat']``).\n        "
        if data is None:
            return None
        data = _unwrap(data, 'chat')
        if not isinstance(data, dict):
            return None
        return cls(chat_id=_to_str(data.get('chat_id')) or '', chat_type=data.get('chat_type', ''), user_id=_to_str(data.get('user_id')), first_name=data.get('first_name'), last_name=data.get('last_name'), title=data.get('title'), username=data.get('username'))
