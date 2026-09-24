"""Shared transport-facing mechanics for Telegram-shaped bot clients.

This module contains the shared request/retry/envelope mechanics plus the
M1-confirmed A-level public methods migrated in M3 and M5. M1 found that
most same-named public methods remain semantically different, so only
identical-logic methods are promoted here.
"""
from __future__ import annotations
import dataclasses
from typing import Any, Callable, Dict, Generic, Mapping, Optional, Protocol, Type, TypeVar, cast
import orjson
from peyk.transport import FilePayload, RetryPolicy, Session, run_with_retry
from peyk.transport.errors import RateLimitedError, TransportError
UserT = TypeVar('UserT')
WebhookInfoT = TypeVar('WebhookInfoT')
FileT = TypeVar('FileT')
ChatT = TypeVar('ChatT')
ChatMemberT = TypeVar('ChatMemberT')
ResultT = TypeVar('ResultT')
ModelT_co = TypeVar('ModelT_co', covariant=True)

class _FromDictModel(Protocol[ModelT_co]):

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional[ModelT_co]:
        """Performs the from dict operation for the shared Telegram-like client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the shared Telegram-like operation."""
        ...
ChatId = int | str

class TelegramLikeClient(Generic[UserT, WebhookInfoT, FileT, ChatT, ChatMemberT]):
    """Base for Bale/Telegram clients sharing request mechanics.

    Only behavior proven identical by the architecture audit belongs here;
    platform-specific methods remain on their concrete clients.
    """
    base_url: str
    _error_class: Type[TransportError]
    max_callback_data_bytes: int = 64
    user_model: type[_FromDictModel[UserT]]
    webhook_info_model: type[_FromDictModel[WebhookInfoT]]
    file_model: type[_FromDictModel[FileT]]
    chat_model: type[_FromDictModel[ChatT]]
    chat_member_parser: Callable[[Optional[dict]], Optional[ChatMemberT]]
    chat_member_count_method: str
    string_media_form_encoded: bool = False
    """Send string media references (``file_id``/URL) form-urlencoded, not as JSON.

    Bale's media methods answer ``400 malformed request`` to a JSON body whose
    media value is a plain string, but accept the same fields as
    ``application/x-www-form-urlencoded`` (hand-verified against
    ``sendAnimation``). Telegram accepts JSON, so the default stays ``False``.
    """

    def __init__(self, token: str, session: Optional[Session]=None, *, retry_policy: Optional[RetryPolicy]=None, logger: object=None, base_url: Optional[str]=None) -> None:
        self._token = token
        self._owns_session = session is None
        self._session = session or Session(logger=logger)
        self._retry_policy = retry_policy or RetryPolicy()
        self._base_url = f'{base_url or self.base_url}/bot{token}'

    @property
    def token(self) -> str:
        """Return the bot token this client was created with (read-only)."""
        return self._token

    async def close(self) -> None:
        """Close only a transport session created by this client.
        
        Returns:
            The operation result (``None``).
        """
        if self._owns_session:
            await self._session.close()

    async def __aenter__(self) -> 'TelegramLikeClient':
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def _parse_error_parameters(self, parameters: object) -> object:
        """Normalize platform-specific error parameters for the error class."""
        return parameters

    def _extract_retry_hint(self, response: object) -> Optional[float]:
        """Return a platform-specific application-level retry hint.

        Bale's audited envelope does not require special handling here and
        therefore returns ``None``.  Telegram can override this hook to map
        ``parameters.retry_after`` to ``RateLimitedError`` without teaching
        the shared base about Telegram-specific response fields.
        """
        return None

    @classmethod
    def _parse_user(cls, result: object) -> UserT:
        return cast(UserT, cls.user_model.from_dict(result))

    @classmethod
    def _parse_webhook_info(cls, result: object) -> WebhookInfoT:
        return cast(WebhookInfoT, cls.webhook_info_model.from_dict(result))

    async def get_me(self) -> UserT:
        """Return the authenticated bot user using the platform's user model.

        Returns:
            The concrete user model configured by the subclass.
        """
        result = await self._call('getMe')
        return self._parse_user(result)

    async def get_webhook_info(self) -> WebhookInfoT:
        """Return webhook status using the platform's webhook-info model.

        Returns:
            The concrete webhook-info model configured by the subclass.
        """
        result = await self._call('getWebhookInfo')
        return self._parse_webhook_info(result)

    async def get_file(self, file_id: str) -> FileT:
        """Fetch the platform's file descriptor for ``file_id``.

        Args:
            file_id: Platform-specific file identifier.

        Returns:
            The concrete file model configured by the subclass.
        """
        result = await self._call('getFile', json_body={'file_id': file_id})
        return cast(FileT, self.file_model.from_dict(result))

    async def delete_message(self, chat_id: ChatId, message_id: int) -> bool:
        """Removes message through the shared Telegram-like API.

Args:
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the shared Telegram-like operation."""
        'Executes the delete_message operation.\n        \n        Args:\n            chat_id: Integer or string chat identifier.\n            message_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``bool``).\n        '
        payload = {'chat_id': chat_id, 'message_id': message_id}
        return bool(await self._call('deleteMessage', json_body=payload))

    async def unban_chat_member(self, chat_id: ChatId, user_id: int, *, only_if_banned: Optional[bool]=None) -> bool:
        """Performs the unban chat member operation for the shared Telegram-like client.

Args:
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.
    only_if_banned: Value used by this operation.

Returns:
    Result produced by the shared Telegram-like operation."""
        'Executes the unban_chat_member operation.\n        \n        Args:\n            chat_id: Integer or string chat identifier.\n            user_id: Value of the declared parameter type.\n            only_if_banned: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``bool``).\n        '
        payload: Dict[str, object] = {'chat_id': chat_id, 'user_id': user_id}
        if only_if_banned is not None:
            payload['only_if_banned'] = only_if_banned
        return bool(await self._call('unbanChatMember', json_body=payload))

    async def unpin_all_chat_messages(self, chat_id: ChatId) -> bool:
        """Performs the unpin all chat messages operation for the shared Telegram-like client.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the shared Telegram-like operation."""
        'Executes the unpin_all_chat_messages operation.\n        \n        Args:\n            chat_id: Integer or string chat identifier.\n        \n        \n        Returns:\n            The operation result (``bool``).\n        '
        return bool(await self._call('unpinAllChatMessages', json_body={'chat_id': chat_id}))

    async def leave_chat(self, chat_id: ChatId) -> bool:
        """Performs the leave chat operation for the shared Telegram-like client.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the shared Telegram-like operation."""
        'Executes the leave_chat operation.\n        \n        Args:\n            chat_id: Integer or string chat identifier.\n        \n        \n        Returns:\n            The operation result (``bool``).\n        '
        return bool(await self._call('leaveChat', json_body={'chat_id': chat_id}))

    async def get_chat(self, chat_id: ChatId) -> ChatT:
        """Return chat information using the platform's chat model.

        Args:
            chat_id: Integer or string identifier accepted by the platform.

        Returns:
            The concrete chat model configured by the subclass.
        """
        result = await self._call('getChat', json_body={'chat_id': chat_id})
        return cast(ChatT, self.chat_model.from_dict(result))

    async def get_chat_member(self, chat_id: ChatId, user_id: int) -> ChatMemberT:
        """Return a member record parsed by the concrete platform adapter.

        Args:
            chat_id: Integer or string chat identifier.
            user_id: User identifier whose membership should be fetched.

        Returns:
            The concrete chat-member type configured by the subclass.
        """
        result = await self._call('getChatMember', json_body={'chat_id': chat_id, 'user_id': user_id})
        return cast(ChatMemberT, type(self).chat_member_parser(result))

    async def _get_chat_member_count(self, chat_id: ChatId) -> int:
        result = await self._call(self.chat_member_count_method, json_body={'chat_id': chat_id})
        return int(result)

    async def set_chat_title(self, chat_id: ChatId, title: str) -> bool:
        """Updates chat title through the shared Telegram-like API.

Args:
    chat_id: Identifier of the target chat.
    title: Title to apply to the target resource.

Returns:
    Result produced by the shared Telegram-like operation."""
        'Executes the set_chat_title operation.\n        \n        Args:\n            chat_id: Integer or string chat identifier.\n            title: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``bool``).\n        '
        return bool(await self._call('setChatTitle', json_body={'chat_id': chat_id, 'title': title}))

    async def delete_chat_photo(self, chat_id: ChatId) -> bool:
        """Removes chat photo through the shared Telegram-like API.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the shared Telegram-like operation."""
        'Executes the delete_chat_photo operation.\n        \n        Args:\n            chat_id: Integer or string chat identifier.\n        \n        \n        Returns:\n            The operation result (``bool``).\n        '
        return bool(await self._call('deleteChatPhoto', json_body={'chat_id': chat_id}))

    @classmethod
    def _build_inline_keyboard_button_payload(cls, text: str, callback_data: str) -> Dict[str, str]:
        cls.validate_callback_data(callback_data)
        return {'text': text, 'callback_data': callback_data}

    async def _call(self, method_name: str, *, json_body: Optional[Mapping[str, object]]=None, data: Optional[Mapping[str, str]]=None, files: Optional[Mapping[str, FilePayload]]=None) -> ResultT:
        """POST a method call, unwrap its common ``ok`` envelope, and return result."""
        url = f'{self._base_url}/{method_name}'

        async def operation():
            """Executes the operation operation.
            
            Returns:
                The operation result (``Any``).
            """
            return await self._session.request('POST', url, json_body=json_body if not files else None, data=data, files=files)
        response = await run_with_retry(operation, self._retry_policy)
        body = response.json
        if not isinstance(body, dict):
            raise self._error_class(f'{method_name}: non-JSON or malformed response body', error_code=response.status, description='<no JSON object body>')
        if not body.get('ok', False):
            description = body.get('description', '')
            retry_after = self._extract_retry_hint(body)
            if retry_after is not None:
                raise RateLimitedError(description or f'{method_name} rate limited', retry_after_seconds=retry_after)
            raise self._error_class(description or f'{method_name} failed', error_code=body.get('error_code', response.status), description=description, parameters=self._parse_error_parameters(body.get('parameters')))
        return cast(ResultT, body.get('result'))

    @classmethod
    def validate_callback_data(cls, data: str) -> None:
        """Performs the validate callback data operation for the shared Telegram-like client.

Args:
    data: Value used by this operation."""
        'Raise ``ValueError`` unless callback data is 1..N UTF-8 bytes.\n                \n                Args:\n                    data: Value of the declared parameter type.\n                \n                \n                Returns:\n                    The operation result (``None``).\n                \n        \n        Raises:\n            ValueError: Raised when the operation cannot complete.\n        '
        encoded_len = len(data.encode('utf-8'))
        if encoded_len < 1 or encoded_len > cls.max_callback_data_bytes:
            raise ValueError(f'callback_data must be 1-{cls.max_callback_data_bytes} bytes (UTF-8 encoded); got {encoded_len} bytes')

    @staticmethod
    def _is_upload(value: object) -> bool:
        """Return whether a media value needs a multipart file part."""
        if isinstance(value, FilePayload):
            return True
        if isinstance(value, (bytes, bytearray)):
            return True
        return hasattr(value, 'read')

    @staticmethod
    def _as_file_payload(value: object, *, default_filename: str) -> FilePayload:
        """Normalize raw upload content to the transport's ``FilePayload``."""
        if isinstance(value, FilePayload):
            return value
        return FilePayload(content=value, filename=default_filename)

    @staticmethod
    def _json_field(value: object) -> str:
        """Serialize a structured value for a multipart string field."""
        return orjson.dumps(value).decode('utf-8')

    @staticmethod
    def _form_field_value(value: object) -> str:
        """Render one multipart form field as a string.

        Strings pass through, structured values (``dict``/``list``/``tuple`` and
        dataclass models such as a rendered ``InlineKeyboardMarkup``) are JSON
        encoded, and everything else falls back to ``str``.  Dataclass models must
        be JSON encoded here: ``str()`` would send their Python ``repr`` and the
        platform silently drops a ``reply_markup`` it cannot parse.
        """
        if isinstance(value, str):
            return value
        if isinstance(value, (dict, list, tuple)) or (dataclasses.is_dataclass(value) and not isinstance(value, type)):
            return orjson.dumps(value).decode('utf-8')
        return str(value)

    @classmethod
    def _build_media_request_kwargs(cls, field_name: str, media: object, *, json_fields: Optional[Mapping[str, object]]=None, form_fields: Optional[Mapping[str, str]]=None, extra_files: Optional[Mapping[str, object]]=None, default_filename: str) -> Dict[str, object]:
        """Build the platform-neutral JSON/multipart request for media.

        Public media APIs remain platform-owned because their parameter
        surfaces differ. This helper shares only the proven mechanics: a
        string media reference stays in JSON (or is form-urlencoded when the
        platform sets ``string_media_form_encoded``, as Bale does), while an upload (or any extra
        upload such as a thumbnail) switches the complete request to
        multipart and normalizes upload values to ``FilePayload``.
        """
        extra_files = extra_files or {}
        needs_multipart = cls._is_upload(media) or any((cls._is_upload(value) for value in extra_files.values()))
        if not needs_multipart:
            payload: Dict[str, object] = dict(json_fields or {})
            payload[field_name] = media
            for key, value in extra_files.items():
                payload[key] = value
            if form_fields:
                payload.update(form_fields)
            if cls.string_media_form_encoded:
                return {'data': {key: cls._form_field_value(value) for key, value in payload.items()}}
            return {'json_body': payload}
        fields: Dict[str, str] = dict(form_fields or {})
        for key, value in (json_fields or {}).items():
            fields[key] = cls._form_field_value(value)
        files: Dict[str, FilePayload] = {field_name: cls._as_file_payload(media, default_filename=default_filename)}
        for key, value in extra_files.items():
            if cls._is_upload(value):
                files[key] = cls._as_file_payload(value, default_filename=f'{key}_{default_filename}')
            else:
                fields[key] = value
        return {'data': fields, 'files': files}

    @classmethod
    def _media_request_kwargs(cls, field_name: str, media: object, *, json_fields: Optional[Mapping[str, object]]=None, form_fields: Optional[Mapping[str, str]]=None, default_filename: str) -> Dict[str, object]:
        """Build shared JSON-vs-multipart kwargs for a single media value.

        A string is a reusable ``file_id``/URL and remains an ordinary JSON
        field.  Bytes, streams, and ``FilePayload`` instances become one
        multipart file part.  ``json_fields`` are JSON-body fields on the
        string path and are JSON-serialized as multipart fields on uploads.
        """
        if cls._is_upload(media):
            fields = dict(form_fields or {})
            for name, value in (json_fields or {}).items():
                fields[name] = cls._json_field(value)
            return {'data': fields, 'files': {field_name: cls._as_file_payload(media, default_filename=default_filename)}}
        payload: Dict[str, object] = dict(json_fields or {})
        payload[field_name] = media
        if form_fields:
            payload.update(form_fields)
        return {'json_body': payload}
