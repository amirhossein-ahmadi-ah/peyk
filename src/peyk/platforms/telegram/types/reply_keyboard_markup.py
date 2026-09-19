from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ReplyKeyboardMarkup:
    """This object represents a custom keyboard with reply options (see Introduction to bots for details and examples). Not supported in channels and for messages sent on behalf of a business account.

Attributes:
    keyboard: Array of button rows, each represented by an Array of KeyboardButton objects
    is_persistent: Requests clients to always show the keyboard when the regular keyboard is hidden. Defaults to False, in which case the custom keyboard can be hidden and opened with a keyboard icon.
    resize_keyboard: Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if there are just two rows of buttons). Defaults to False, in which case the custom keyboard is always of the same height as the app's standard keyboard.
    one_time_keyboard: Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available, but clients will automatically display the usual letter-keyboard in the chat - the user can press a special button in the input field to see the custom keyboard again. Defaults to False.
    input_field_placeholder: The placeholder to be shown in the input field when the keyboard is active; 1-64 characters
    selective: Use this parameter if you want to show the keyboard to specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message.

Example: A user requests to change the bot's language, bot replies to the request with a keyboard to select the new language. Other users in the group don't see the keyboard."""
    keyboard: List[List[Union[KeyboardButton, Mapping[str, object], str]]] = field(default_factory=list)
    is_persistent: Optional[bool] = None
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ReplyKeyboardMarkup']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ReplyKeyboardMarkup']``).\n        "
        if data is None:
            return None
        return cls(keyboard=data.get('keyboard', []) or [], is_persistent=data.get('is_persistent'), resize_keyboard=data.get('resize_keyboard'), one_time_keyboard=data.get('one_time_keyboard'), input_field_placeholder=data.get('input_field_placeholder'), selective=data.get('selective'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'keyboard': [_button_row_to_dict(row) for row in self.keyboard]}
        if self.is_persistent is not None:
            body['is_persistent'] = self.is_persistent
        if self.resize_keyboard is not None:
            body['resize_keyboard'] = self.resize_keyboard
        if self.one_time_keyboard is not None:
            body['one_time_keyboard'] = self.one_time_keyboard
        if self.input_field_placeholder is not None:
            body['input_field_placeholder'] = self.input_field_placeholder
        if self.selective is not None:
            body['selective'] = self.selective
        return body
