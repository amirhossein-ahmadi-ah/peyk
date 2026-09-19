from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class ButtonSelection:
    """Represent the Rubika Bot API ``ButtonSelection`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    selection_id: str = ''
    search_type: str = ButtonSelectionSearchEnum.NONE
    get_type: str = ButtonSelectionGetEnum.LOCAL
    items: List[ButtonSelectionItem] = field(default_factory=list)
    is_multi_selection: bool = False
    columns_count: str = '1'
    title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ButtonSelection']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ButtonSelection']``).\n        "
        from .button_selection_item import ButtonSelectionItem
        if data is None:
            return None
        return cls(selection_id=_to_str(data.get('selection_id')) or '', search_type=data.get('search_type', ButtonSelectionSearchEnum.NONE), get_type=data.get('get_type', ButtonSelectionGetEnum.LOCAL), items=[i for i in (ButtonSelectionItem.from_dict(x) for x in data.get('items') or []) if i is not None], is_multi_selection=bool(data.get('is_multi_selection', False)), columns_count=_to_str(data.get('columns_count')) or '1', title=data.get('title'))

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'selection_id': self.selection_id, 'search_type': self.search_type, 'get_type': self.get_type, 'items': [i.to_dict() for i in self.items], 'is_multi_selection': self.is_multi_selection, 'columns_count': self.columns_count, 'title': self.title}
