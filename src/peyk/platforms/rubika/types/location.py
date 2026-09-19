from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Location:
    """Represent the Rubika Bot API ``Location`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    latitude: Optional[str] = None
    longitude: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Location']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Location']``).\n        "
        if data is None:
            return None
        return cls(latitude=_to_str(data.get('latitude')), longitude=_to_str(data.get('longitude')))
