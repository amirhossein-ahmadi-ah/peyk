from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class LabeledPrice:
    """This object represents a portion of the price for goods or services.

Attributes:
    label: Portion label
    amount: Price of the product in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies)."""
    label: str
    amount: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['LabeledPrice']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['LabeledPrice']``).\n        "
        if data is None:
            return None
        return cls(label=data.get('label', ''), amount=data.get('amount', 0))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'label': self.label, 'amount': self.amount}
