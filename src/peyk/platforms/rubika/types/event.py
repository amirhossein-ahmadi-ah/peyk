from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Event:
    """Represent the Rubika Bot API ``Event`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    type: Optional[str] = None
    access_list: Optional[List[str]] = None
    join_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Event']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Event']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type'), access_list=list(data.get('access_list') or []) or None, join_type=data.get('join_type'))
