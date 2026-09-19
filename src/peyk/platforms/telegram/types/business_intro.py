from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BusinessIntro:
    """Contains information about the start page settings of a Telegram Business account.

Attributes:
    title: Title text of the business intro
    message: Message text of the business intro
    sticker: Sticker of the business intro"""
    title: Optional[str] = None
    message: Optional[str] = None
    sticker: Optional[Sticker] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BusinessIntro']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BusinessIntro']``).\n        "
        if data is None:
            return None
        return cls(title=_parse_api_value('String', data.get('title')), message=_parse_api_value('String', data.get('message')), sticker=_parse_api_value('Sticker', data.get('sticker')))
