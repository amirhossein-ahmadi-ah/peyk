from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputInvoiceMessageContent:
    """Represents the content of an invoice message to be sent as the result of an inline query.

Attributes:
    title: Product name, 1-32 characters
    description: Product description, 1-255 characters
    payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.
    currency: Three-letter ISO 4217 currency code, see more on currencies. Pass 'XTR' for payments in Telegram Stars.
    prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars.
    provider_token: Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.
    max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
    suggested_tip_amounts: A JSON-serialized Array of suggested amounts of tip in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
    provider_data: A JSON-serialized object for data about the invoice, which will be shared with the payment provider. A detailed description of the required fields should be provided by the payment provider.
    photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service.
    photo_size: Photo size in bytes
    photo_width: Photo width
    photo_height: Photo height
    need_name: Pass True if you require the user's full name to complete the order. Ignored for payments in Telegram Stars.
    need_phone_number: Pass True if you require the user's phone number to complete the order. Ignored for payments in Telegram Stars.
    need_email: Pass True if you require the user's email address to complete the order. Ignored for payments in Telegram Stars.
    need_shipping_address: Pass True if you require the user's shipping address to complete the order. Ignored for payments in Telegram Stars.
    send_phone_number_to_provider: Pass True if the user's phone number should be sent to the provider. Ignored for payments in Telegram Stars.
    send_email_to_provider: Pass True if the user's email address should be sent to the provider. Ignored for payments in Telegram Stars.
    is_flexible: Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars."""
    title: str
    description: str
    payload: str
    currency: str
    prices: Sequence[Union[LabeledPrice, Mapping[str, object]]] = field(default_factory=list)
    provider_token: Optional[str] = None
    max_tip_amount: Optional[int] = None
    suggested_tip_amounts: Optional[List[int]] = None
    provider_data: Optional[str] = None
    photo_url: Optional[str] = None
    photo_size: Optional[int] = None
    photo_width: Optional[int] = None
    photo_height: Optional[int] = None
    need_name: Optional[bool] = None
    need_phone_number: Optional[bool] = None
    need_email: Optional[bool] = None
    need_shipping_address: Optional[bool] = None
    send_phone_number_to_provider: Optional[bool] = None
    send_email_to_provider: Optional[bool] = None
    is_flexible: Optional[bool] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'title': self.title, 'description': self.description, 'payload': self.payload, 'currency': self.currency, 'prices': [p.to_dict() if isinstance(p, LabeledPrice) else dict(p) for p in self.prices]}
        if self.provider_token is not None:
            body['provider_token'] = self.provider_token
        if self.max_tip_amount is not None:
            body['max_tip_amount'] = self.max_tip_amount
        if self.suggested_tip_amounts is not None:
            body['suggested_tip_amounts'] = self.suggested_tip_amounts
        if self.provider_data is not None:
            body['provider_data'] = self.provider_data
        if self.photo_url is not None:
            body['photo_url'] = self.photo_url
        if self.photo_size is not None:
            body['photo_size'] = self.photo_size
        if self.photo_width is not None:
            body['photo_width'] = self.photo_width
        if self.photo_height is not None:
            body['photo_height'] = self.photo_height
        if self.need_name is not None:
            body['need_name'] = self.need_name
        if self.need_phone_number is not None:
            body['need_phone_number'] = self.need_phone_number
        if self.need_email is not None:
            body['need_email'] = self.need_email
        if self.need_shipping_address is not None:
            body['need_shipping_address'] = self.need_shipping_address
        if self.send_phone_number_to_provider is not None:
            body['send_phone_number_to_provider'] = self.send_phone_number_to_provider
        if self.send_email_to_provider is not None:
            body['send_email_to_provider'] = self.send_email_to_provider
        if self.is_flexible is not None:
            body['is_flexible'] = self.is_flexible
        return body
