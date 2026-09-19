from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class InlineMessage:
    """Represent the Rubika Bot API ``InlineMessage`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    sender_id: str = ''
    text: Optional[str] = None
    file: Optional[File] = None
    location: Optional[Location] = None
    aux_data: Optional[AuxData] = None
    message_id: str = ''
    chat_id: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InlineMessage']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InlineMessage']``).\n        "
        from .aux_data import AuxData
        from .file import File
        from .location import Location
        if data is None:
            return None
        data = _unwrap(data, 'inline_message')
        if not isinstance(data, dict):
            return None
        return cls(sender_id=_to_str(data.get('sender_id')) or '', text=data.get('text'), file=File.from_dict(data.get('file')), location=Location.from_dict(data.get('location')), aux_data=AuxData.from_dict(data.get('aux_data')), message_id=_to_str(data.get('message_id')) or '', chat_id=_to_str(data.get('chat_id')) or '')
