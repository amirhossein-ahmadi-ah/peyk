from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineKeyboardButton:
    """This object represents one button of an inline keyboard. Exactly one of the fields other than text, icon_custom_emoji_id, and style must be used to specify the type of the button.

Attributes:
    text: Label text on the button
    icon_custom_emoji_id: Unique identifier of the custom emoji shown before the text of the button. Can only be used by bots that purchased additional usernames on Fragment or in the messages directly sent by the bot to private, group and supergroup chats if the owner of the bot has a Telegram Premium subscription.
    style: Style of the button. Must be one of 'danger' (red), 'success' (green) or 'primary' (blue). If omitted, then an app-specific style is used.
    url: HTTP or tg:// URL to be opened when the button is pressed. Links tg://user?id= can be used to mention a user by their identifier without using a username, if this is allowed by their privacy settings.
    callback_data: Data to be sent in a callback query to the bot when the button is pressed, 1-64 bytes
    web_app: Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Available only in private chats between a user and the bot. Not supported for messages sent on behalf of a business account.
    login_url: An HTTPS URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget.
    switch_inline_query: If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot's username and the specified inline query in the input field. May be empty, in which case just the bot's username will be inserted. Not supported for messages sent in channel direct messages chats and on behalf of a business account.
    switch_inline_query_current_chat: If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field. May be empty, in which case only the bot's username will be inserted.

This offers a quick way for the user to open your bot in inline mode in the same chat - good for selecting something from multiple options. Not supported in channels and for messages sent in channel direct messages chats and on behalf of a business account.
    switch_inline_query_chosen_chat: If set, pressing the button will prompt the user to select one of their chats of the specified type, open that chat and insert the bot's username and the specified inline query in the input field. Not supported for messages sent in channel direct messages chats and on behalf of a business account.
    copy_text: Description of the button that copies the specified text to the clipboard
    callback_game: Description of the game that will be launched when the user presses the button.

NOTE: This type of button must always be the first button in the first row.
    pay: Specify True, to send a Pay button. Substrings '' and 'XTR' in the buttons's text will be replaced with a Telegram Star icon.

NOTE: This type of button must always be the first button in the first row and can only be used in invoice messages."""
    text: str = ''
    icon_custom_emoji_id: Optional[str] = None
    style: Optional[str] = None
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[WebAppInfo] = None
    login_url: Optional[LoginUrl] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = None
    copy_text: Optional[CopyTextButton] = None
    callback_game: Optional[CallbackGame] = None
    pay: Optional[bool] = None
    disabled: Optional[DisabledButton] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InlineKeyboardButton']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InlineKeyboardButton']``).\n        "
        if data is None:
            return None
        return cls(text=data.get('text', ''), icon_custom_emoji_id=data.get('icon_custom_emoji_id'), style=data.get('style'), url=data.get('url'), callback_data=data.get('callback_data'), web_app=WebAppInfo.from_dict(data.get('web_app')), login_url=LoginUrl.from_dict(data.get('login_url')), switch_inline_query=data.get('switch_inline_query'), switch_inline_query_current_chat=data.get('switch_inline_query_current_chat'), switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat.from_dict(data.get('switch_inline_query_chosen_chat')), copy_text=CopyTextButton.from_dict(data.get('copy_text')), callback_game=CallbackGame.from_dict(data.get('callback_game')), pay=data.get('pay'), disabled=DisabledButton.from_dict(data.get('disabled')))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        if self.callback_data is not None:
            validate_callback_data(self.callback_data)
        body: Dict[str, object] = {'text': self.text}
        if self.icon_custom_emoji_id is not None:
            body['icon_custom_emoji_id'] = self.icon_custom_emoji_id
        if self.style is not None:
            body['style'] = self.style
        if self.url is not None:
            body['url'] = self.url
        if self.callback_data is not None:
            body['callback_data'] = self.callback_data
        if self.web_app is not None:
            body['web_app'] = self.web_app.to_dict()
        if self.login_url is not None:
            body['login_url'] = self.login_url.to_dict()
        if self.switch_inline_query is not None:
            body['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            body['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.switch_inline_query_chosen_chat is not None:
            body['switch_inline_query_chosen_chat'] = self.switch_inline_query_chosen_chat.to_dict()
        if self.copy_text is not None:
            body['copy_text'] = self.copy_text.to_dict()
        if self.callback_game is not None:
            body['callback_game'] = self.callback_game.to_dict()
        if self.pay is not None:
            body['pay'] = self.pay
        if self.disabled is not None:
            body['disabled'] = self.disabled.to_dict()
        return body
