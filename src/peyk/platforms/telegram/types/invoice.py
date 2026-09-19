from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Invoice:
    """This object contains basic information about an invoice.

Attributes:
    title: Product name
    description: Product description
    start_parameter: Unique bot deep-linking parameter that can be used to generate this invoice
    currency: Three-letter ISO 4217 currency code, or 'XTR' for payments in Telegram Stars
    total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies)."""
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Invoice']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Invoice']``).\n        "
        if data is None:
            return None
        return cls(title=_parse_api_value('String', data.get('title')), description=_parse_api_value('String', data.get('description')), start_parameter=_parse_api_value('String', data.get('start_parameter')), currency=_parse_api_value('String', data.get('currency')), total_amount=_parse_api_value('Integer', data.get('total_amount')))
