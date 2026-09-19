from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Bot:
    """Represent the Rubika Bot API ``Bot`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    bot_id: str = ''
    bot_title: str = ''
    avatar: Optional[File] = None
    description: Optional[str] = None
    username: Optional[str] = None
    start_message: Optional[str] = None
    share_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Bot']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Bot']``).\n        "
        from .file import File
        if data is None:
            return None
        data = _unwrap(data, 'bot')
        if not isinstance(data, dict):
            return None
        return cls(bot_id=_to_str(data.get('bot_id')) or '', bot_title=data.get('bot_title', ''), avatar=File.from_dict(data.get('avatar')), description=data.get('description'), username=data.get('username'), start_message=data.get('start_message'), share_url=data.get('share_url'))
