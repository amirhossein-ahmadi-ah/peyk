from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class KeyboardButton:
    """This object represents one button of the reply keyboard. At most one of the fields other than text, icon_custom_emoji_id, and style must be used to specify the type of the button. For simple text buttons, String can be used instead of this object to specify the button text.

Attributes:
    text: Text of the button. If none of the fields other than text, icon_custom_emoji_id, and style are used, it will be sent as a message when the button is pressed.
    icon_custom_emoji_id: Unique identifier of the custom emoji shown before the text of the button. Can only be used by bots that purchased additional usernames on Fragment or in the messages directly sent by the bot to private, group and supergroup chats if the owner of the bot has a Telegram Premium subscription.
    style: Style of the button. Must be one of 'danger' (red), 'success' (green) or 'primary' (blue). If omitted, then an app-specific style is used.
    request_users: If specified, pressing the button will open a list of suitable users. Identifiers of selected users will be sent to the bot in a 'users_shared' service message. Available in private chats only.
    request_chat: If specified, pressing the button will open a list of suitable chats. Tapping on a chat will send its identifier to the bot in a 'chat_shared' service message. Available in private chats only.
    request_managed_bot: If specified, pressing the button will ask the user to create and share a bot that will be managed by the current bot. Available for bots that enabled management of other bots in the @BotFather Mini App. Available in private chats only.
    request_contact: If True, the user's phone number will be sent as a contact when the button is pressed. Available in private chats only.
    request_location: If True, the user's current location will be sent when the button is pressed. Available in private chats only.
    request_poll: If specified, the user will be asked to create a poll and send it to the bot when the button is pressed. Available in private chats only.
    web_app: If specified, the described Web App will be launched when the button is pressed. The Web App will be able to send a 'web_app_data' service message. Available in private chats only.
    request_user: If specified, pressing the button will open a list of suitable users. Tapping on any user will send their identifier to the bot in a 'user_shared' service message. Available in private chats only."""
    text: str = ''
    icon_custom_emoji_id: Optional[str] = None
    style: Optional[str] = None
    request_users: Optional[KeyboardButtonRequestUsers] = None
    request_chat: Optional[KeyboardButtonRequestChat] = None
    request_managed_bot: Optional[KeyboardButtonRequestManagedBot] = None
    request_contact: Optional[bool] = None
    request_location: Optional[bool] = None
    request_poll: Optional[KeyboardButtonPollType] = None
    web_app: Optional[WebAppInfo] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['KeyboardButton']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['KeyboardButton']``).\n        "
        if data is None:
            return None
        return cls(text=data.get('text', ''), icon_custom_emoji_id=data.get('icon_custom_emoji_id'), style=data.get('style'), request_users=KeyboardButtonRequestUsers.from_dict(data.get('request_users')), request_chat=KeyboardButtonRequestChat.from_dict(data.get('request_chat')), request_managed_bot=KeyboardButtonRequestManagedBot.from_dict(data.get('request_managed_bot')), request_contact=data.get('request_contact'), request_location=data.get('request_location'), request_poll=KeyboardButtonPollType.from_dict(data.get('request_poll')), web_app=WebAppInfo.from_dict(data.get('web_app')))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'text': self.text}
        if self.icon_custom_emoji_id is not None:
            body['icon_custom_emoji_id'] = self.icon_custom_emoji_id
        if self.style is not None:
            body['style'] = self.style
        if self.request_users is not None:
            body['request_users'] = self.request_users.to_dict()
        if self.request_chat is not None:
            body['request_chat'] = self.request_chat.to_dict()
        if self.request_managed_bot is not None:
            body['request_managed_bot'] = self.request_managed_bot.to_dict()
        if self.request_contact is not None:
            body['request_contact'] = self.request_contact
        if self.request_location is not None:
            body['request_location'] = self.request_location
        if self.request_poll is not None:
            body['request_poll'] = self.request_poll.to_dict()
        if self.web_app is not None:
            body['web_app'] = self.web_app.to_dict()
        return body
