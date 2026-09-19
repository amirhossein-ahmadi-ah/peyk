from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
import orjson
from peyk.transport import FilePayload
from ..errors import TelegramAPIError, ResponseParameters
from ..models import *
from .. import models as _models
globals().update({k: v for k, v in vars(_models).items() if k.startswith('_')})
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def create_invoice_link(self, title: str, description: str, payload: str, currency: str, prices: List[LabeledPrice], *, business_connection_id: Optional[str]=None, provider_token: Optional[str]=None, subscription_period: Optional[int]=None, max_tip_amount: Optional[int]=None, suggested_tip_amounts: Optional[List[int]]=None, provider_data: Optional[str]=None, photo_url: Optional[str]=None, photo_size: Optional[int]=None, photo_width: Optional[int]=None, photo_height: Optional[int]=None, need_name: Optional[bool]=None, need_phone_number: Optional[bool]=None, need_email: Optional[bool]=None, need_shipping_address: Optional[bool]=None, send_phone_number_to_provider: Optional[bool]=None, send_email_to_provider: Optional[bool]=None, is_flexible: Optional[bool]=None) -> str:
    """Use this method to create a link for an invoice. Returns the created invoice link as String on success.

Args:
    title: Product name, 1-32 characters
    description: Product description, 1-255 characters
    payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use it for your internal processes.
    currency: Three-letter ISO 4217 currency code, see more on currencies. Pass 'XTR' for payments in Telegram Stars.
    prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in Telegram Stars.
    business_connection_id: Unique identifier of the business connection on behalf of which the link will be created. For payments in Telegram Stars only.
    provider_token: Payment provider token, obtained via @BotFather. Pass an empty string for payments in Telegram Stars.
    subscription_period: The number of seconds the subscription will be active for before the next payment. The currency must be set to 'XTR' (Telegram Stars) if the parameter is used. Currently, it must always be 2592000 (30 days) if specified. Any number of subscriptions can be active for a given bot at the same time, including multiple concurrent subscriptions from the same user. Subscription price must no exceed 10000 Telegram Stars.
    max_tip_amount: The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in Telegram Stars.
    suggested_tip_amounts: A JSON-serialized Array of suggested amounts of tips in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
    provider_data: JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
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
    is_flexible: Pass True if the final price depends on the shipping method. Ignored for payments in Telegram Stars.

Returns:
    str: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if title is not None:
        payload['title'] = _serialize_api_value(title)
    if description is not None:
        payload['description'] = _serialize_api_value(description)
    if payload is not None:
        payload['payload'] = _serialize_api_value(payload)
    if provider_token is not None:
        payload['provider_token'] = _serialize_api_value(provider_token)
    if currency is not None:
        payload['currency'] = _serialize_api_value(currency)
    if prices is not None:
        payload['prices'] = _serialize_api_value(prices)
    if subscription_period is not None:
        payload['subscription_period'] = _serialize_api_value(subscription_period)
    if max_tip_amount is not None:
        payload['max_tip_amount'] = _serialize_api_value(max_tip_amount)
    if suggested_tip_amounts is not None:
        payload['suggested_tip_amounts'] = _serialize_api_value(suggested_tip_amounts)
    if provider_data is not None:
        payload['provider_data'] = _serialize_api_value(provider_data)
    if photo_url is not None:
        payload['photo_url'] = _serialize_api_value(photo_url)
    if photo_size is not None:
        payload['photo_size'] = _serialize_api_value(photo_size)
    if photo_width is not None:
        payload['photo_width'] = _serialize_api_value(photo_width)
    if photo_height is not None:
        payload['photo_height'] = _serialize_api_value(photo_height)
    if need_name is not None:
        payload['need_name'] = _serialize_api_value(need_name)
    if need_phone_number is not None:
        payload['need_phone_number'] = _serialize_api_value(need_phone_number)
    if need_email is not None:
        payload['need_email'] = _serialize_api_value(need_email)
    if need_shipping_address is not None:
        payload['need_shipping_address'] = _serialize_api_value(need_shipping_address)
    if send_phone_number_to_provider is not None:
        payload['send_phone_number_to_provider'] = _serialize_api_value(send_phone_number_to_provider)
    if send_email_to_provider is not None:
        payload['send_email_to_provider'] = _serialize_api_value(send_email_to_provider)
    if is_flexible is not None:
        payload['is_flexible'] = _serialize_api_value(is_flexible)
    result = await self._call('createInvoiceLink', json_body=payload)
    return _parse_api_result('str', result)
