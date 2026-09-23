from __future__ import annotations
from typing import Dict, Mapping, Union

from ..types.chat_permissions import ChatPermissions


async def restrict_chat_member(self, chat_id: Union[int, str], user_id: int, permissions: Union[ChatPermissions, Mapping[str, object]]) -> bool:
    """Restrict a member of a group or supergroup.

    The bot must be an administrator with the right to restrict members. To lift
    a restriction, send the permissions you want the user to have (``True``).

    Bale has no ``until_date``: the restriction lasts until you lift it yourself,
    so a timed mute must be undone manually at the right time.

    Args:
        chat_id: Identifier of the target chat.
        user_id: Identifier of the target user.
        permissions: New permissions, as a ``ChatPermissions`` or a plain mapping.

    Returns:
        bool: ``True`` when Bale accepted the request.

    Raises:
        BaleAPIError: If the Bale API rejects the request.

    Example:
        ``await client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))``
    """
    serialized: Dict[str, object] = permissions.to_dict() if isinstance(permissions, ChatPermissions) else dict(permissions)
    payload: Dict[str, object] = {'chat_id': chat_id, 'user_id': user_id, 'permissions': serialized}
    return bool(await self._call('restrictChatMember', json_body=payload))
