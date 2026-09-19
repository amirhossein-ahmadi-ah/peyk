from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Optional, Union

async def promote_chat_member(self, chat_id: Union[int, str], user_id: int, *, can_change_info: Optional[bool]=None, can_post_messages: Optional[bool]=None, can_edit_messages: Optional[bool]=None, can_delete_messages: Optional[bool]=None, can_manage_video_chats: Optional[bool]=None, can_invite_users: Optional[bool]=None, can_restrict_members: Optional[bool]=None) -> bool:
    """Performs the promote chat member operation for the Bale client.

Args:
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.
    can_change_info: Value used by this operation.
    can_post_messages: Value used by this operation.
    can_edit_messages: Value used by this operation.
    can_delete_messages: Value used by this operation.
    can_manage_video_chats: Value used by this operation.
    can_invite_users: Value used by this operation.
    can_restrict_members: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Promote or demote a chat member. Pass all rights `False` to demote.\n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        user_id: Value of the declared parameter type.\n        can_change_info: Value of the declared parameter type.\n        can_post_messages: Value of the declared parameter type.\n        can_edit_messages: Value of the declared parameter type.\n        can_delete_messages: Value of the declared parameter type.\n        can_manage_video_chats: Value of the declared parameter type.\n        can_invite_users: Value of the declared parameter type.\n        can_restrict_members: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    '
    payload: Dict[str, object] = {'chat_id': chat_id, 'user_id': user_id}
    optional_rights = {'can_change_info': can_change_info, 'can_post_messages': can_post_messages, 'can_edit_messages': can_edit_messages, 'can_delete_messages': can_delete_messages, 'can_manage_video_chats': can_manage_video_chats, 'can_invite_users': can_invite_users, 'can_restrict_members': can_restrict_members}
    for key, value in optional_rights.items():
        if value is not None:
            payload[key] = value
    return bool(await self._call('promoteChatMember', json_body=payload))
