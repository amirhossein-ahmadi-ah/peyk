from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Transaction

async def inquire_transaction(self, transaction_id: str) -> Transaction:
    """Performs the inquire transaction operation for the Bale client.

Args:
    transaction_id: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Query the status of a wallet transaction.\n    \n            Per docs.bale.ai, returns a `Transaction` object with the\n            current status of the specified transaction.\n            \n    \n    Args:\n        transaction_id: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Transaction``).\n    '
    payload = {'transaction_id': transaction_id}
    result = await self._call('inquireTransaction', json_body=payload)
    return Transaction.from_dict(result)
