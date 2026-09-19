from __future__ import annotations

from ..errors import BaleAPIError
from peyk.transport import FilePayload

async def logout(self) -> bool:
    """Log the bot out of the cloud API server before running locally.
    
            Wraps `logout` (no parameters). See docs.bale.ai: intended to be
            called before running the bot against a local/test environment.
            
    
    Returns:
        The operation result (``bool``).
    """
    return bool(await self._call('logout'))
