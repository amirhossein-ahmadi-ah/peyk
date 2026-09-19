from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class SuccessfulPayment:
    """A confirmed successful payment."""
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuccessfulPayment']:
        """Parse raw Bale data into ``SuccessfulPayment``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[SuccessfulPayment]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(currency=data.get('currency', ''), total_amount=data.get('total_amount', 0), invoice_payload=data.get('invoice_payload', ''), telegram_payment_charge_id=data.get('telegram_payment_charge_id', ''), provider_payment_charge_id=data.get('provider_payment_charge_id', ''))
