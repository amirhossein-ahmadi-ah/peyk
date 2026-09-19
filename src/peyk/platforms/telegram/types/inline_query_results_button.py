from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultsButton:
    """This object represents a button to be shown above inline query results. You must use exactly one of the optional fields.

Attributes:
    text: Label text on the button
    web_app: Description of the Web App that will be launched when the user presses the button. The Web App will be able to switch back to the inline mode using the method switchInlineQuery inside the Web App.
    start_parameter: Deep-linking parameter for the /start message sent to the bot when a user presses the button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.

Example: An inline bot that sends YouTube videos can ask the user to connect the bot to their YouTube account to adapt search results accordingly. To do this, it displays a 'Connect your YouTube account' button above the results, or even before showing any. The user presses the button, switches to a private chat with the bot and, in doing so, passes a start parameter that instructs the bot to return an OAuth link. Once done, the bot can offer a switch_inline button so that the user can easily return to the chat where they wanted to use the bot's inline capabilities."""
    text: str
    web_app: Optional[Union[WebAppInfo, Mapping[str, object]]] = None
    start_parameter: Optional[str] = None

    def __post_init__(self) -> None:
        if (self.web_app is None) == (self.start_parameter is None):
            raise ValueError("InlineQueryResultsButton requires exactly one of 'web_app' / 'start_parameter'")

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InlineQueryResultsButton']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InlineQueryResultsButton']``).\n        "
        if data is None:
            return None
        web_app = data.get('web_app')
        return cls(text=data.get('text', ''), web_app=WebAppInfo.from_dict(web_app) if isinstance(web_app, dict) else web_app, start_parameter=data.get('start_parameter'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'text': self.text}
        if self.web_app is not None:
            if isinstance(self.web_app, WebAppInfo):
                body['web_app'] = self.web_app.to_dict()
            else:
                body['web_app'] = dict(self.web_app)
        if self.start_parameter is not None:
            body['start_parameter'] = self.start_parameter
        return body
