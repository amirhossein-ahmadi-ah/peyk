from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class TransactionPartnerOther:
    """Describes a transaction with an unknown source or recipient.

Attributes:
    type: Type of the transaction partner, always 'other'"""
    type: str = 'other'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['TransactionPartnerOther']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['TransactionPartnerOther']``).\n        "
        if data is None:
            return None
        return cls(type=_parse_api_value('String', data.get('type')))
