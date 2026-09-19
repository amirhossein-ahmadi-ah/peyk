from __future__ import annotations

from ..errors import BaleAPIError
from peyk.transport import FilePayload

async def close_bot(self) -> bool:
    """Close the bot before moving it from one server to another.
    
            Wraps the API's `close` method -- renamed here to avoid shadowing
            this class's own `close()`, which closes the local transport
            session and is unrelated to this API call. See the module
            docstring for details.
            
    
    Returns:
        The operation result (``bool``).
    """
    return bool(await self._call('close'))
