from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Message:
    """Represent the Rubika Bot API ``Message`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    message_id: str = ''
    text: Optional[str] = None
    time: Optional[int] = None
    is_edited: bool = False
    sender_type: Optional[str] = None
    sender_id: Optional[str] = None
    aux_data: Optional[AuxData] = None
    file: Optional[File] = None
    reply_to_message_id: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    forwarded_no_link: Optional[str] = None
    location: Optional[Location] = None
    sticker: Optional[Sticker] = None
    contact_message: Optional[ContactMessage] = None
    poll: Optional[Poll] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Message']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Message']``).\n        "
        from .aux_data import AuxData
        from .contact_message import ContactMessage
        from .file import File
        from .forwarded_from import ForwardedFrom
        from .location import Location
        from .poll import Poll
        from .sticker import Sticker
        if data is None:
            return None
        return cls(message_id=_to_str(data.get('message_id')) or '', text=data.get('text'), time=_to_int(data.get('time')), is_edited=bool(data.get('is_edited', False)), sender_type=data.get('sender_type'), sender_id=_to_str(data.get('sender_id')), aux_data=AuxData.from_dict(data.get('aux_data')), file=File.from_dict(data.get('file')), reply_to_message_id=_to_str(data.get('reply_to_message_id')), forwarded_from=ForwardedFrom.from_dict(data.get('forwarded_from')), forwarded_no_link=data.get('forwarded_no_link'), location=Location.from_dict(data.get('location')), sticker=Sticker.from_dict(data.get('sticker')), contact_message=ContactMessage.from_dict(data.get('contact_message')), poll=Poll.from_dict(data.get('poll')))
