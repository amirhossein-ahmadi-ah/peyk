from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def promote_chat_member(self, chat_id: ChatId, user_id: int, *, is_anonymous: Optional[bool]=None, can_manage_chat: Optional[bool]=None, can_delete_messages: Optional[bool]=None, can_manage_video_chats: Optional[bool]=None, can_restrict_members: Optional[bool]=None, can_promote_members: Optional[bool]=None, can_change_info: Optional[bool]=None, can_invite_users: Optional[bool]=None, can_post_stories: Optional[bool]=None, can_edit_stories: Optional[bool]=None, can_delete_stories: Optional[bool]=None, can_post_messages: Optional[bool]=None, can_edit_messages: Optional[bool]=None, can_pin_messages: Optional[bool]=None, can_manage_topics: Optional[bool]=None, can_manage_direct_messages: Optional[bool]=None, can_manage_tags: Optional[bool]=None, can_send_welcome_messages: Optional[bool]=None) -> bool:
    """Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Pass False for all boolean parameters to demote a user. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    user_id: Unique identifier of the target user
    is_anonymous: Pass True if the administrator's presence in the chat is hidden
    can_manage_chat: Pass True if the administrator can access the chat event log, get boost list, see hidden supergroup and channel members, report spam messages, ignore slow mode, and send messages to the chat without paying Telegram Stars. Implied by any other administrator privilege.
    can_delete_messages: Pass True if the administrator can delete messages of other users
    can_manage_video_chats: Pass True if the administrator can manage video chats
    can_restrict_members: Pass True if the administrator can restrict, ban or unban chat members, or access supergroup statistics. For backward compatibility, defaults to True for promotions of channel administrators.
    can_promote_members: Pass True if the administrator can add new administrators with a subset of their own privileges or demote administrators that they have promoted, directly or indirectly (promoted by administrators that were appointed by him)
    can_change_info: Pass True if the administrator can change chat title, photo and other settings
    can_invite_users: Pass True if the administrator can invite new users to the chat
    can_post_stories: Pass True if the administrator can post stories to the chat
    can_edit_stories: Pass True if the administrator can edit stories posted by other users, post stories to the chat page, pin chat stories, and access the chat's story archive
    can_delete_stories: Pass True if the administrator can delete stories posted by other users
    can_post_messages: Pass True if the administrator can post messages in the channel, approve suggested posts, or access channel statistics; for channels only
    can_edit_messages: Pass True if the administrator can edit messages of other users and can pin messages; for channels only
    can_pin_messages: Pass True if the administrator can pin messages; for supergroups only
    can_manage_topics: Pass True if the user is allowed to create, rename, close, and reopen forum topics; for supergroups only
    can_manage_direct_messages: Pass True if the administrator can manage direct messages within the channel and decline suggested posts; for channels only
    can_manage_tags: Pass True if the administrator can edit the tags of regular members; for groups and supergroups only
    can_send_welcome_messages: Value accepted by this operation.

Returns:
    bool: Result returned by Telegram on successful execution."""
    rights = ChatAdministratorRights(is_anonymous=is_anonymous, can_manage_chat=can_manage_chat, can_delete_messages=can_delete_messages, can_manage_video_chats=can_manage_video_chats, can_restrict_members=can_restrict_members, can_promote_members=can_promote_members, can_change_info=can_change_info, can_invite_users=can_invite_users, can_post_stories=can_post_stories, can_edit_stories=can_edit_stories, can_delete_stories=can_delete_stories, can_post_messages=can_post_messages, can_edit_messages=can_edit_messages, can_pin_messages=can_pin_messages, can_manage_topics=can_manage_topics, can_manage_direct_messages=can_manage_direct_messages, can_manage_tags=can_manage_tags, can_send_welcome_messages=can_send_welcome_messages)
    payload: Dict[str, object] = {'chat_id': chat_id, 'user_id': user_id, **rights.to_dict()}
    return bool(await self._call('promoteChatMember', json_body=payload))
