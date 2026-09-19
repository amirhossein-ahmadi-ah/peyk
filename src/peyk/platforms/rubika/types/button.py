from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Button:
    """A single button.

    Structure per the official docs: base fields (id, type,
    button_text) plus exactly one nested ``button_*`` object whose
    name depends on the ``type``.
    """
    id: str = ''
    type: str = ButtonTypeEnum.SIMPLE
    button_text: str = ''
    button_selection: Optional[ButtonSelection] = None
    button_calendar: Optional[ButtonCalendar] = None
    button_number_picker: Optional[ButtonNumberPicker] = None
    button_string_picker: Optional[ButtonStringPicker] = None
    button_location: Optional[ButtonLocation] = None
    button_textbox: Optional[ButtonTextbox] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Button']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Button']``).\n        "
        from .button_calendar import ButtonCalendar
        from .button_location import ButtonLocation
        from .button_number_picker import ButtonNumberPicker
        from .button_selection import ButtonSelection
        from .button_string_picker import ButtonStringPicker
        from .button_textbox import ButtonTextbox
        if data is None:
            return None
        return cls(id=_to_str(data.get('id')) or '', type=data.get('type', ButtonTypeEnum.SIMPLE), button_text=data.get('button_text', ''), button_selection=ButtonSelection.from_dict(data.get('button_selection')), button_calendar=ButtonCalendar.from_dict(data.get('button_calendar')), button_number_picker=ButtonNumberPicker.from_dict(data.get('button_number_picker')), button_string_picker=ButtonStringPicker.from_dict(data.get('button_string_picker')), button_location=ButtonLocation.from_dict(data.get('button_location')), button_textbox=ButtonTextbox.from_dict(data.get('button_textbox')))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'id': self.id, 'type': self.type, 'button_text': self.button_text}
        if self.button_selection is not None:
            body['button_selection'] = self.button_selection.to_dict()
        if self.button_calendar is not None:
            body['button_calendar'] = self.button_calendar.to_dict()
        if self.button_number_picker is not None:
            body['button_number_picker'] = self.button_number_picker.to_dict()
        if self.button_string_picker is not None:
            body['button_string_picker'] = self.button_string_picker.to_dict()
        if self.button_location is not None:
            body['button_location'] = self.button_location.to_dict()
        if self.button_textbox is not None:
            body['button_textbox'] = self.button_textbox.to_dict()
        return body
