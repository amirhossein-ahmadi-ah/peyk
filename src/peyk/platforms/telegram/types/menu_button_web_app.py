from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MenuButtonWebApp:
    """Represents a menu button, which launches a Web App.

Attributes:
    type: Type of the button, must be web_app
    text: Text on the button
    web_app: Description of the Web App that will be launched when the user presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. Alternatively, a t.me link to a Web App of the bot can be specified in the object instead of the Web App's URL, in which case the Web App will be opened as if the user pressed the link."""
    type: str = 'web_app'
    text: str = ''
    web_app: Optional[WebAppInfo] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MenuButtonWebApp']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MenuButtonWebApp']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'web_app'), text=data.get('text', ''), web_app=WebAppInfo.from_dict(data.get('web_app')))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'text': self.text}
        if self.web_app is not None:
            body['web_app'] = self.web_app.to_dict()
        return body
