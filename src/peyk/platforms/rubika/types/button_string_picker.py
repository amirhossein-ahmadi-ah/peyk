from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ButtonStringPicker:
    """Represent the Rubika Bot API ``ButtonStringPicker`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    items: List[str] = field(default_factory=list)
    default_value: Optional[str] = None
    title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ButtonStringPicker']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ButtonStringPicker']``).\n        "
        if data is None:
            return None
        return cls(items=list(data.get('items') or []), default_value=data.get('default_value'), title=data.get('title'))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'items': list(self.items)}
        if self.default_value is not None:
            body['default_value'] = self.default_value
        if self.title is not None:
            body['title'] = self.title
        return body
