from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload

async def ask_review(self, user_id: int, delay_seconds: int) -> bool:
    """Performs the ask review operation for the Bale client.

Args:
    user_id: Identifier of the target user.
    delay_seconds: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    "Request a user to rate or review the bot.\n    \n            Per docs.bale.ai (Aban 1404): this feature is only available\n            in newer client versions -- if the user's client doesn't support\n            it, the review form is simply not displayed. No error is raised.\n    \n            `user_id`: the user to prompt.\n            `delay_seconds`: seconds to wait after calling before showing the form.\n            \n    \n    Args:\n        user_id: Value of the declared parameter type.\n        delay_seconds: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    "
    payload = {'user_id': user_id, 'delay_seconds': delay_seconds}
    return bool(await self._call('askReview', json_body=payload))
