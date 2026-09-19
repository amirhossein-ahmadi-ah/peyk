"""Rubika client compatibility facade.

The public API methods live in :mod:`peyk.platforms.rubika.methods`, one
module per method. This facade preserves the historical import path and
client class while keeping lifecycle/request-envelope helpers coherent.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union

from peyk.transport import RetryPolicy, Session, run_with_retry

from .errors import RubikaAPIError, error_for_envelope
from .models import *
from .methods import *

RUBIKA_BASE_URL = "https://botapi.rubika.ir/v3"


class RubikaClient:
    """A typed asynchronous wrapper around the Rubika Bot API.

    Rubika requests use wrapped response envelopes. File sending follows the
    audited three-step upload flow, and update polling uses Rubika's
    ``offset_id`` cursor rather than Telegram's numeric update offset.
    """

    base_url: str = RUBIKA_BASE_URL

    def __init__(self, token: str, session: Optional[Session] = None, *, retry_policy: Optional[RetryPolicy] = None, logger: object = None, base_url: Optional[str] = None) -> None:
        """Initialize the client while preserving the original session ownership contract.

        Args:
            token: Rubika bot token.
            session: Optional existing transport session.
            retry_policy: Optional transport retry policy.
            logger: Optional logger for a newly-created session.
            base_url: Optional API base URL override.

        Returns:
            None.
        """
        self._token = token
        self._owns_session = session is None
        self._session = session or Session(logger=logger)
        self._retry_policy = retry_policy or RetryPolicy()
        self._base_url = f"{(base_url or self.base_url).rstrip('/')}/{token}"

    async def __aenter__(self) -> "RubikaClient":
        """Enter the async context manager and return this client."""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Exit the async context manager and close the client."""
        await self.close()

    async def _call(self, method_name: str, *, json_body: Optional[Dict[str, object]] = None) -> object:
        """Execute one Rubika request and validate its response envelope.

        Args:
            method_name: Rubika API method name.
            json_body: JSON request payload.

        Returns:
            Any: The response envelope's ``data`` value.

        Raises:
            RubikaAPIError: If the response is malformed or reports an API error.
        """
        url = f"{self._base_url}/{method_name}"

        async def operation():
            """Executes the operation operation.
            
            Returns:
                The operation result (``Any``).
            """
            return await self._session.request(
                "POST", url, json_body=json_body if json_body is not None else {}
            )

        response = await run_with_retry(operation, self._retry_policy)
        envelope = response.json
        if not isinstance(envelope, dict):
            raise RubikaAPIError(
                f"{method_name}: non-JSON or malformed response body",
                error_code="INVALID_RESPONSE",
                error_message="<no JSON object body>",
                raw=None,
            )
        if envelope.get("status", "") != "OK":
            raise error_for_envelope(envelope)
        return envelope.get("data")

    @staticmethod
    def _keypad_to_dict(keypad: Union[Keypad, Dict[str, object], None]) -> Optional[Dict[str, object]]:
        """Normalize a keypad object or mapping into an API dictionary."""
        if keypad is None:
            return None
        if isinstance(keypad, Keypad):
            return keypad.to_dict()
        return dict(keypad)

    @staticmethod
    def _commands_to_list(commands: List[Union[BotCommand, Dict[str, object]]]) -> List[Dict[str, object]]:
        """Normalize command objects or mappings into the API list shape."""
        return [c.to_dict() if isinstance(c, BotCommand) else dict(c) for c in commands]

    close = close
    _call = _call
    _keypad_to_dict = _keypad_to_dict
    _commands_to_list = _commands_to_list
    get_me = get_me
    send_message = send_message
    send_poll = send_poll
    send_location = send_location
    send_contact = send_contact
    get_chat = get_chat
    get_updates = get_updates
    forward_message = forward_message
    edit_message_text = edit_message_text
    edit_message_keypad = edit_message_keypad
    delete_message = delete_message
    set_commands = set_commands
    update_bot_endpoints = update_bot_endpoints
    edit_chat_keypad = edit_chat_keypad
    remove_chat_keypad = remove_chat_keypad
    get_file = get_file
    send_file = send_file
    request_send_file = request_send_file
    upload_file = upload_file
    upload_and_send_file = upload_and_send_file
    ban_chat_member = ban_chat_member
    unban_chat_member = unban_chat_member
    _parse_message_id_response = _parse_message_id_response


__all__ = ["RubikaClient", "RUBIKA_BASE_URL"]
