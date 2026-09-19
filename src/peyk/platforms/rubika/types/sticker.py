from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Sticker:
    """Represent the Rubika Bot API ``Sticker`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    sticker_id: str = ''
    file: Optional[File] = None
    emoji_character: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Sticker']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Sticker']``).\n        "
        from .file import File
        if data is None:
            return None
        return cls(sticker_id=_to_str(data.get('sticker_id')) or '', file=File.from_dict(data.get('file')), emoji_character=data.get('emoji_character'))
