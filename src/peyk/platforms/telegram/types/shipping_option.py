from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ShippingOption:
    """This object represents one shipping option.

Attributes:
    id: Shipping option identifier
    title: Option title
    prices: List of price portions"""
    id: str
    title: str
    prices: List[LabeledPrice]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ShippingOption']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ShippingOption']``).\n        "
        if data is None:
            return None
        return cls(id=_parse_api_value('String', data.get('id')), title=_parse_api_value('String', data.get('title')), prices=_parse_api_value('Array of LabeledPrice', data.get('prices')))
