from __future__ import annotations

from ..errors import BaleAPIError
from peyk.transport import FilePayload

async def delete_webhook(self) -> bool:
    """Delete the webhook and switch back to `getUpdates`.
    
            Per docs.bale.ai, takes no parameters. Returns `True` on success.
            
    
    Returns:
        The operation result (``bool``).
    """
    return bool(await self._call('deleteWebhook'))
