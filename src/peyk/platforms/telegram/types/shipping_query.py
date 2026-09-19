from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ShippingQuery:
    """This object contains information about an incoming shipping query.

Attributes:
    id: Unique query identifier
    from: User who sent the query
    invoice_payload: Bot-specified invoice payload
    shipping_address: User specified shipping address"""
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ShippingQuery']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ShippingQuery']``).\n        "
        if data is None:
            return None
        return cls(id=_parse_api_value('String', data.get('id')), from_=_parse_api_value('User', data.get('from')), invoice_payload=_parse_api_value('String', data.get('invoice_payload')), shipping_address=_parse_api_value('ShippingAddress', data.get('shipping_address')))
