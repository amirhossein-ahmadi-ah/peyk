from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Update
from typing import Any, Dict, List, Optional

async def get_updates(self, *, offset: Optional[int]=None, limit: Optional[int]=None, timeout: Optional[int]=None) -> List[Update]:
    """Retrieves updates from the Bale API.

Args:
    offset: Pagination offset returned by the preceding request.
    limit: Maximum number of results requested.
    timeout: Maximum time to wait for the operation.

Returns:
    Result produced by the Bale operation."""
    'Implement Bale client method ``get_updates``.\n\nArgs:\n    Uses the parameter values documented by the method signature.\n\nReturns:\n    The value returned by the Bale API after parsing.\n\nRaises:\n    BaleAPIError: If the Bale API rejects the request.\n\nExample:\n    ``await client.get_updates(... )``'
    payload: Dict[str, object] = {}
    if offset is not None:
        payload['offset'] = offset
    if limit is not None:
        payload['limit'] = limit
    if timeout is not None:
        payload['timeout'] = timeout
    result = await self._call('getUpdates', json_body=payload)
    return Update.list_from_result(result)
