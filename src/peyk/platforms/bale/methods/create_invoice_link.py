from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Mapping, Sequence

async def create_invoice_link(self, title: str, description: str, payload_: str, provider_token: str, prices: Sequence[Mapping[str, object]]) -> str:
    """Creates invoice link through the Bale API.

Args:
    title: Title to apply to the target resource.
    description: Description to apply to the target resource.
    payload_: Value used by this operation.
    provider_token: Value used by this operation.
    prices: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Create a payment link for use in Mini Apps.\n    \n            Per docs.bale.ai, creates a new wallet payment link and returns\n            its string ID on success.\n            \n    \n    Args:\n        title: Value of the declared parameter type.\n        description: Value of the declared parameter type.\n        payload_: Value of the declared parameter type.\n        provider_token: Value of the declared parameter type.\n        prices: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``str``).\n    '
    body: Dict[str, object] = {'title': title, 'description': description, 'payload': payload_, 'provider_token': provider_token, 'prices': list(prices)}
    result = await self._call('createInvoiceLink', json_body=body)
    return str(result)
