from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Optional

async def answer_pre_checkout_query(self, pre_checkout_query_id: str, ok: bool, *, error_message: Optional[str]=None) -> bool:
    """Answers the pre checkout query request through the Bale API.

Args:
    pre_checkout_query_id: Value used by this operation.
    ok: Value used by this operation.
    error_message: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Respond to a pre-checkout query.\n    \n            Per docs.bale.ai, the bot must respond within **10 seconds** of\n            receiving the pre-checkout query update, or the payment is cancelled.\n    \n            `pre_checkout_query_id`: the unique query ID.\n            `ok`: True to confirm the payment is acceptable, False to reject.\n            `error_message`: required if `ok` is False -- the reason shown\n            to the user for why the payment cannot proceed.\n            \n    \n    Args:\n        pre_checkout_query_id: Value of the declared parameter type.\n        ok: Value of the declared parameter type.\n        error_message: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    '
    payload: Dict[str, object] = {'pre_checkout_query_id': pre_checkout_query_id, 'ok': ok}
    if error_message is not None:
        payload['error_message'] = error_message
    return bool(await self._call('answerPreCheckoutQuery', json_body=payload))
