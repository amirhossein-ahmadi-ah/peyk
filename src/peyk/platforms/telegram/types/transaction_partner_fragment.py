from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class TransactionPartnerFragment:
    """Describes a withdrawal transaction with Fragment.

Attributes:
    type: Type of the transaction partner, always 'fragment'
    withdrawal_state: State of the transaction if the transaction is outgoing"""
    type: str = 'fragment'
    withdrawal_state: Optional[RevenueWithdrawalState] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['TransactionPartnerFragment']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['TransactionPartnerFragment']``).\n        "
        if data is None:
            return None
        return cls(type=_parse_api_value('String', data.get('type')), withdrawal_state=_parse_api_value('RevenueWithdrawalState', data.get('withdrawal_state')))
