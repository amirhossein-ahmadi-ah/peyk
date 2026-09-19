from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class GetUpdatesResult:
    """Wrapper for the getUpdates response payload.

    Confirmed from the official docs: the ``data`` field carries both
    ``updates`` (list) and ``next_offset_id`` (the offset to pass on
    the next call).
    """
    updates: List[Update] = field(default_factory=list)
    next_offset_id: Optional[str] = None

    @classmethod
    def from_data(cls, data: object) -> 'GetUpdatesResult':
        """Performs the from data operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_data operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'GetUpdatesResult'``).\n        "
        from .update import Update
        if data is None:
            return cls()
        if isinstance(data, list):
            return cls(updates=[u for u in (Update.from_dict(x) for x in data) if u])
        if isinstance(data, dict):
            updates_raw = data.get('updates') or []
            return cls(updates=[u for u in (Update.from_dict(x) for x in updates_raw) if u], next_offset_id=_to_str(data.get('next_offset_id')))
        return cls()
