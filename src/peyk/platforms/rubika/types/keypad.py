from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Keypad:
    """Represent the Rubika Bot API ``Keypad`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    rows: List[KeypadRow] = field(default_factory=list)
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'rows': [r.to_dict() for r in self.rows]}
        if self.resize_keyboard is not None:
            body['resize_keyboard'] = self.resize_keyboard
        if self.one_time_keyboard is not None:
            body['one_time_keyboard'] = self.one_time_keyboard
        return body

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Keypad']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Keypad']``).\n        "
        from .keypad_row import KeypadRow
        if data is None:
            return None
        return cls(rows=[r for r in (KeypadRow.from_dict(x) for x in data.get('rows') or []) if r is not None], resize_keyboard=data.get('resize_keyboard'), one_time_keyboard=data.get('one_time_keyboard'))
