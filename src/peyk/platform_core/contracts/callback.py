"""Normalized callback/button and payment-query contracts."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Union
Identifier = Union[int, str]

@dataclass(frozen=True)
class IncomingCallbackQuery:
    """Normalized inline/reply-button press.

    Telegram/Bale ``callback_data`` and Rubika ``aux_data.button_id`` are both
    exposed as ``data``.  Rubika does not provide a callback-query ID, so its
    ``id`` is honestly None.
    """
    id: Optional[str] = None
    from_user_id: Optional[Identifier] = None
    chat_id: Optional[Identifier] = None
    message_id: Optional[Identifier] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    raw: object = None

@dataclass(frozen=True)
class IncomingPreCheckoutQuery:
    """IncomingPreCheckoutQuery provides the platform-core API surface used by peyk."""
    'Represents `IncomingPreCheckoutQuery`.\n\nRaises:\n    \n'
    id: Optional[str] = None
    from_user_id: Optional[Identifier] = None
    currency: Optional[str] = None
    total_amount: Optional[int] = None
    invoice_payload: Optional[str] = None
    shipping_option_id: Optional[str] = None
    order_info: object = None
    raw: object = None

@dataclass(frozen=True)
class IncomingShippingQuery:
    """IncomingShippingQuery provides the platform-core API surface used by peyk."""
    'Represents `IncomingShippingQuery`.\n\nRaises:\n    \n'
    id: Optional[str] = None
    from_user_id: Optional[Identifier] = None
    invoice_payload: Optional[str] = None
    shipping_address: object = None
    raw: object = None
