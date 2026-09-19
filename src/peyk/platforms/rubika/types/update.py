from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Update:
    """Represent the Rubika Bot API ``Update`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    type: Optional[str] = None
    chat_id: Optional[str] = None
    removed_message_id: Optional[str] = None
    new_message: Optional[Message] = None
    updated_message: Optional[Message] = None
    event_data: Optional[Event] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Update']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Update']``).\n        "
        from .event import Event
        from .message import Message
        if data is None:
            return None
        data = _unwrap(data, 'update')
        if not isinstance(data, dict):
            return None
        return cls(type=data.get('type'), chat_id=_to_str(data.get('chat_id')), removed_message_id=_to_str(data.get('removed_message_id')), new_message=Message.from_dict(data.get('new_message')), updated_message=Message.from_dict(data.get('updated_message')), event_data=Event.from_dict(data.get('event_data')))
