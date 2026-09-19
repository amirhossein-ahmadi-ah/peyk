from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ButtonNumberPicker:
    """Represent the Rubika Bot API ``ButtonNumberPicker`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    min_value: str = '0'
    max_value: str = '100'
    default_value: Optional[str] = None
    title: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ButtonNumberPicker']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ButtonNumberPicker']``).\n        "
        if data is None:
            return None
        return cls(min_value=_to_str(data.get('min_value')) or '0', max_value=_to_str(data.get('max_value')) or '100', default_value=data.get('default_value'), title=data.get('title', ''))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'min_value': self.min_value, 'max_value': self.max_value, 'title': self.title}
        if self.default_value is not None:
            body['default_value'] = self.default_value
        return body
