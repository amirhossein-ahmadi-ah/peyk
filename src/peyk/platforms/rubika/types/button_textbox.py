from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ButtonTextbox:
    """Represent the Rubika Bot API ``ButtonTextbox`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    type_line: str = ButtonTextboxTypeLineEnum.SINGLE_LINE
    type_keypad: str = ButtonTextboxTypeKeypadEnum.STRING
    place_holder: Optional[str] = None
    title: Optional[str] = None
    default_value: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ButtonTextbox']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ButtonTextbox']``).\n        "
        if data is None:
            return None
        return cls(type_line=data.get('type_line', ButtonTextboxTypeLineEnum.SINGLE_LINE), type_keypad=data.get('type_keypad', ButtonTextboxTypeKeypadEnum.STRING), place_holder=data.get('place_holder'), title=data.get('title'), default_value=data.get('default_value'))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type_line': self.type_line, 'type_keypad': self.type_keypad}
        if self.place_holder is not None:
            body['place_holder'] = self.place_holder
        if self.title is not None:
            body['title'] = self.title
        if self.default_value is not None:
            body['default_value'] = self.default_value
        return body
