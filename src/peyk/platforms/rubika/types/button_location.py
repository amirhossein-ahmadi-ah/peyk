from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ButtonLocation:
    """Represent the Rubika Bot API ``ButtonLocation`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    default_pointer_location: Optional[Location] = None
    default_map_location: Optional[Location] = None
    type: str = ButtonLocationTypeEnum.PICKER
    title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ButtonLocation']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ButtonLocation']``).\n        "
        from .location import Location
        if data is None:
            return None
        return cls(default_pointer_location=Location.from_dict(data.get('default_pointer_location')), default_map_location=Location.from_dict(data.get('default_map_location')), type=data.get('type', ButtonLocationTypeEnum.PICKER), title=data.get('title'))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type}
        if self.default_pointer_location is not None:
            body['default_pointer_location'] = {'latitude': self.default_pointer_location.latitude, 'longitude': self.default_pointer_location.longitude}
        if self.default_map_location is not None:
            body['default_map_location'] = {'latitude': self.default_map_location.latitude, 'longitude': self.default_map_location.longitude}
        if self.title is not None:
            body['title'] = self.title
        return body
