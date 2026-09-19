from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class TransactionPartnerTelegramApi:
    """Describes a transaction with payment for paid broadcasting.

Attributes:
    type: Type of the transaction partner, always 'telegram_api'
    request_count: The number of successful requests that exceeded regular limits and were therefore billed"""
    type: str = 'telegram_api'
    request_count: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['TransactionPartnerTelegramApi']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['TransactionPartnerTelegramApi']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'telegram_api'), request_count=data.get('request_count', 0))
