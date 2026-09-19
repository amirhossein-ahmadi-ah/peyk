from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ButtonCalendar:
    """Represent the Rubika Bot API ``ButtonCalendar`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    default_value: Optional[str] = None
    type: str = ButtonCalendarTypeEnum.DATE_PERSIAN
    min_year: str = '1300'
    max_year: str = '1450'
    title: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ButtonCalendar']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ButtonCalendar']``).\n        "
        if data is None:
            return None
        return cls(default_value=data.get('default_value'), type=data.get('type', ButtonCalendarTypeEnum.DATE_PERSIAN), min_year=_to_str(data.get('min_year')) or '1300', max_year=_to_str(data.get('max_year')) or '1450', title=data.get('title', ''))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'min_year': self.min_year, 'max_year': self.max_year, 'title': self.title}
        if self.default_value is not None:
            body['default_value'] = self.default_value
        return body
