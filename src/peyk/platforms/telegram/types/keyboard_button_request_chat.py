from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class KeyboardButtonRequestChat:
    """This object defines the criteria used to request a suitable chat. Information about the selected chat will be shared with the bot when the corresponding button is pressed. The bot will be granted requested rights in the chat if appropriate..

Attributes:
    request_id: Signed 32-bit identifier of the request, which will be received back in the ChatShared object. Must be unique within the message.
    chat_is_channel: Pass True to request a channel chat, pass False to request a group or a supergroup chat
    chat_is_forum: Pass True to request a forum supergroup, pass False to request a non-forum chat. If not specified, no additional restrictions are applied.
    chat_has_username: Pass True to request a supergroup or a channel with a username, pass False to request a chat without a username. If not specified, no additional restrictions are applied.
    chat_is_created: Pass True to request a chat owned by the user. Otherwise, no additional restrictions are applied.
    user_administrator_rights: A JSON-serialized object listing the required administrator rights of the user in the chat. The rights must be a superset of bot_administrator_rights. If not specified, no additional restrictions are applied.
    bot_administrator_rights: A JSON-serialized object listing the required administrator rights of the bot in the chat. The rights must be a subset of user_administrator_rights. If not specified, no additional restrictions are applied.
    bot_is_member: Pass True to request a chat with the bot as a member. Otherwise, no additional restrictions are applied.
    request_title: Pass True to request the chat's title
    request_username: Pass True to request the chat's username
    request_photo: Pass True to request the chat's photo"""
    request_id: int = 0
    chat_is_channel: bool = False
    chat_is_forum: Optional[bool] = None
    chat_has_username: Optional[bool] = None
    chat_is_created: Optional[bool] = None
    user_administrator_rights: Optional[ChatAdministratorRights] = None
    bot_administrator_rights: Optional[ChatAdministratorRights] = None
    bot_is_member: Optional[bool] = None
    request_title: Optional[bool] = None
    request_username: Optional[bool] = None
    request_photo: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['KeyboardButtonRequestChat']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['KeyboardButtonRequestChat']``).\n        "
        if data is None:
            return None
        return cls(request_id=data.get('request_id', 0), chat_is_channel=data.get('chat_is_channel', False), chat_is_forum=data.get('chat_is_forum'), chat_has_username=data.get('chat_has_username'), chat_is_created=data.get('chat_is_created'), user_administrator_rights=ChatAdministratorRights.from_dict(data.get('user_administrator_rights')), bot_administrator_rights=ChatAdministratorRights.from_dict(data.get('bot_administrator_rights')), bot_is_member=data.get('bot_is_member'), request_title=data.get('request_title'), request_username=data.get('request_username'), request_photo=data.get('request_photo'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'request_id': self.request_id, 'chat_is_channel': self.chat_is_channel}
        if self.chat_is_forum is not None:
            body['chat_is_forum'] = self.chat_is_forum
        if self.chat_has_username is not None:
            body['chat_has_username'] = self.chat_has_username
        if self.chat_is_created is not None:
            body['chat_is_created'] = self.chat_is_created
        if self.user_administrator_rights is not None:
            body['user_administrator_rights'] = self.user_administrator_rights.to_dict()
        if self.bot_administrator_rights is not None:
            body['bot_administrator_rights'] = self.bot_administrator_rights.to_dict()
        if self.bot_is_member is not None:
            body['bot_is_member'] = self.bot_is_member
        if self.request_title is not None:
            body['request_title'] = self.request_title
        if self.request_username is not None:
            body['request_username'] = self.request_username
        if self.request_photo is not None:
            body['request_photo'] = self.request_photo
        return body
