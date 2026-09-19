from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class StarTransactions:
    """Contains a list of Telegram Star transactions.

Attributes:
    transactions: The list of transactions"""
    transactions: List[StarTransaction]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['StarTransactions']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['StarTransactions']``).\n        "
        if data is None:
            return None
        return cls(transactions=_parse_api_value('Array of StarTransaction', data.get('transactions')))
