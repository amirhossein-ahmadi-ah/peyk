from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class PollStatus:
    """Represent the Rubika Bot API ``PollStatus`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    state: str = PollStatusEnum.OPEN
    selection_index: int = -1
    percent_vote_options: Optional[List[int]] = None
    total_vote: int = 0
    show_total_votes: bool = False

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PollStatus']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PollStatus']``).\n        "
        if data is None:
            return None
        return cls(state=data.get('state', PollStatusEnum.OPEN), selection_index=_to_int(data.get('selection_index')) or -1, percent_vote_options=list(data.get('percent_vote_options') or []) or None, total_vote=_to_int(data.get('total_vote')) or 0, show_total_votes=bool(data.get('show_total_votes', False)))
