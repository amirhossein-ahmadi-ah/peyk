from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from ._helpers import _to_str, _to_int, _to_float, _unwrap
from ..enums import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum

@dataclass
class Metadata:
    """Represent the Rubika Bot API ``Metadata`` type.

    The class preserves the existing public fields and wire-format behavior.
    """
    meta_data_parts: List[MetadataPart] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Metadata']:
        """Performs the from dict operation for the Rubika client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Metadata']``).\n        "
        from .metadata_part import MetadataPart
        if data is None:
            return None
        return cls(meta_data_parts=[p for p in (MetadataPart.from_dict(x) for x in data.get('meta_data_parts') or []) if p is not None])

    def to_dict(self) -> Dict[str, object]:
        """Performs the to dict operation for the Rubika client.

Returns:
    Result produced by the Rubika operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'meta_data_parts': [p.to_dict() for p in self.meta_data_parts]}
