"""Capability-aware cross-platform keyboard builder.

The builder exposes a common button API plus explicit Rubika button types.
Rubika has substantially more button types than Telegram/Bale; those methods
are intentionally platform-specific and fail loudly when another target is
selected.
"""
from __future__ import annotations
import warnings
warnings.warn('peyk.utils.KeyboardBuilder is deprecated; use peyk.keyboard builders.', DeprecationWarning, stacklevel=2)
from dataclasses import dataclass
from typing import Optional
from peyk.platform_core.adapters import BALE_CAPABILITIES, RUBIKA_CAPABILITIES, TELEGRAM_CAPABILITIES
from peyk.platform_core.contracts import PlatformCapabilities
from peyk.platform_core.capabilities import CapabilitySet

class KeyboardBuildError(ValueError):
    """Raised when a keyboard cannot be represented for the target platform."""

@dataclass(frozen=True)
class _ButtonSpec:
    text: str
    callback_data: Optional[str] = None
    url: Optional[str] = None
    kind: str = 'Simple'
    payload: Optional[dict[str, object]] = None
_CAPABILITIES = {'telegram': TELEGRAM_CAPABILITIES, 'bale': BALE_CAPABILITIES, 'rubika': RUBIKA_CAPABILITIES}
_RUBIKA_TYPES = {'Selection', 'Calendar', 'NumberPicker', 'StringPicker', 'Location', 'CameraImage', 'CameraVideo', 'GalleryImage', 'GalleryVideo', 'File', 'Audio', 'RecordAudio', 'Textbox', 'Link', 'AskMyPhoneNumber', 'AskMyLocation', 'Barcode'}

def _normalize_target(target: str | PlatformCapabilities | CapabilitySet) -> tuple[str, PlatformCapabilities]:
    if isinstance(target, CapabilitySet):
        return (target.platform, _CAPABILITIES[target.platform])
    if isinstance(target, PlatformCapabilities):
        if target.platform in _CAPABILITIES:
            return (target.platform, target)
        for name, capabilities in _CAPABILITIES.items():
            if capabilities == target:
                return (name, target)
        return ('custom', target)
    key = target.lower()
    if key not in _CAPABILITIES:
        raise ValueError(f'unknown keyboard target: {target!r}')
    return (key, _CAPABILITIES[key])

class KeyboardBuilder:
    """Build inline/keypad keyboards for Telegram, Bale and Rubika."""

    def __init__(self) -> None:
        self._rows: list[list[_ButtonSpec]] = [[]]

    def button(self, text: str, *, callback_data: str | None=None, url: str | None=None) -> 'KeyboardBuilder':
        """Performs the button operation for the utility client.

Args:
    text: Text content supplied to the operation.
    callback_data: Value used by this operation.
    url: Target URL.

Returns:
    Result produced by the utility operation."""
        "Executes the button operation.\n                \n                Args:\n                    text: Value of the declared parameter type.\n                    callback_data: Value of the declared parameter type.\n                    url: Value of the declared parameter type.\n                \n                \n                Returns:\n                    The operation result (``'KeyboardBuilder'``).\n                \n        \n        Raises:\n            KeyboardBuildError: Raised when the operation cannot complete.\n        "
        if callback_data is not None and url is not None:
            raise KeyboardBuildError('a button cannot have both callback_data and url')
        self._require_text(text)
        self._rows[-1].append(_ButtonSpec(text=text, callback_data=callback_data, url=url, kind='Link' if url else 'Simple'))
        return self

    def url(self, text: str, url: str) -> 'KeyboardBuilder':
        """Performs the url operation for the utility client.

Args:
    text: Text content supplied to the operation.
    url: Target URL.

Returns:
    Result produced by the utility operation."""
        "Executes the url operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            url: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self.button(text, url=url)

    def row(self) -> 'KeyboardBuilder':
        """Performs the row operation for the utility client.

Returns:
    Result produced by the utility operation."""
        "Executes the row operation.\n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        if self._rows[-1]:
            self._rows.append([])
        return self

    def _rubika(self, kind: str, text: str, *, button_id: str | None=None, **payload: object) -> 'KeyboardBuilder':
        if kind not in _RUBIKA_TYPES:
            raise KeyboardBuildError(f'unsupported Rubika button type: {kind}')
        self._require_text(text)
        self._rows[-1].append(_ButtonSpec(text=text, callback_data=button_id, kind=kind, payload=payload or None))
        return self

    def selection(self, text: str, *, button_id: str, selection_id: str, items: list[dict[str, object]] | None=None, search_type: str='None', get_type: str='Local', is_multi_selection: bool=False, columns_count: str='1', title: str | None=None) -> 'KeyboardBuilder':
        """Performs the selection operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.
    selection_id: Value used by this operation.
    items: Value used by this operation.
    search_type: Value used by this operation.
    get_type: Value used by this operation.
    is_multi_selection: Value used by this operation.
    columns_count: Value used by this operation.
    title: Title to apply to the target resource.

Returns:
    Result produced by the utility operation."""
        "Executes the selection operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n            selection_id: Value of the declared parameter type.\n            items: Value of the declared parameter type.\n            search_type: Value of the declared parameter type.\n            get_type: Value of the declared parameter type.\n            is_multi_selection: Value of the declared parameter type.\n            columns_count: Value of the declared parameter type.\n            title: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('Selection', text, button_id=button_id, selection_id=selection_id, items=items or [], search_type=search_type, get_type=get_type, is_multi_selection=is_multi_selection, columns_count=columns_count, title=title or text)

    def calendar(self, text: str, *, button_id: str | None=None, default_value: str | None=None, calendar_type: str='DatePersian', min_year: str='1300', max_year: str='1450') -> 'KeyboardBuilder':
        """Performs the calendar operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.
    default_value: Value used by this operation.
    calendar_type: Value used by this operation.
    min_year: Value used by this operation.
    max_year: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the calendar operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n            default_value: Value of the declared parameter type.\n            calendar_type: Value of the declared parameter type.\n            min_year: Value of the declared parameter type.\n            max_year: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('Calendar', text, button_id=button_id, default_value=default_value, type=calendar_type, min_year=min_year, max_year=max_year, title=text)

    def number_picker(self, text: str, *, button_id: str | None=None, min_value: str='0', max_value: str='100', default_value: str | None=None) -> 'KeyboardBuilder':
        """Performs the number picker operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.
    min_value: Value used by this operation.
    max_value: Value used by this operation.
    default_value: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the number_picker operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n            min_value: Value of the declared parameter type.\n            max_value: Value of the declared parameter type.\n            default_value: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('NumberPicker', text, button_id=button_id, min_value=min_value, max_value=max_value, default_value=default_value, title=text)

    def string_picker(self, text: str, *, button_id: str, items: list[str], default_value: str | None=None) -> 'KeyboardBuilder':
        """Performs the string picker operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.
    items: Value used by this operation.
    default_value: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the string_picker operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n            items: Value of the declared parameter type.\n            default_value: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('StringPicker', text, button_id=button_id, items=items, default_value=default_value, title=text)

    def location(self, text: str, *, button_id: str, location_type: str='Picker', title: str | None=None, default_pointer_location: object=None, default_map_location: object=None) -> 'KeyboardBuilder':
        """Performs the location operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.
    location_type: Value used by this operation.
    title: Title to apply to the target resource.
    default_pointer_location: Value used by this operation.
    default_map_location: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the location operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n            location_type: Value of the declared parameter type.\n            title: Value of the declared parameter type.\n            default_pointer_location: Value of the declared parameter type.\n            default_map_location: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('Location', text, button_id=button_id, type=location_type, title=title or text, default_pointer_location=default_pointer_location, default_map_location=default_map_location)

    def camera_image(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the camera image operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the camera_image operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('CameraImage', text, button_id=button_id)

    def camera_video(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the camera video operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the camera_video operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('CameraVideo', text, button_id=button_id)

    def gallery_image(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the gallery image operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the gallery_image operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('GalleryImage', text, button_id=button_id)

    def gallery_video(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the gallery video operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the gallery_video operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('GalleryVideo', text, button_id=button_id)

    def file(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the file operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the file operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('File', text, button_id=button_id)

    def audio(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the audio operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the audio operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('Audio', text, button_id=button_id)

    def record_audio(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the record audio operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the record_audio operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('RecordAudio', text, button_id=button_id)

    def textbox(self, text: str, *, button_id: str, type_line: str='SingleLine', type_keypad: str='String', place_holder: str | None=None, title: str | None=None, default_value: str | None=None) -> 'KeyboardBuilder':
        """Performs the textbox operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.
    type_line: Value used by this operation.
    type_keypad: Value used by this operation.
    place_holder: Value used by this operation.
    title: Title to apply to the target resource.
    default_value: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the textbox operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n            type_line: Value of the declared parameter type.\n            type_keypad: Value of the declared parameter type.\n            place_holder: Value of the declared parameter type.\n            title: Value of the declared parameter type.\n            default_value: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('Textbox', text, button_id=button_id, type_line=type_line, type_keypad=type_keypad, place_holder=place_holder, title=title or text, default_value=default_value)

    def rubika_link(self, text: str, *, button_id: str, url: str) -> 'KeyboardBuilder':
        """Performs the rubika link operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.
    url: Target URL.

Returns:
    Result produced by the utility operation."""
        "Executes the rubika_link operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n            url: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('Link', text, button_id=button_id, url=url)

    def ask_my_phone_number(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the ask my phone number operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the ask_my_phone_number operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('AskMyPhoneNumber', text, button_id=button_id)

    def ask_my_location(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the ask my location operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the ask_my_location operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('AskMyLocation', text, button_id=button_id)

    def barcode(self, text: str, *, button_id: str) -> 'KeyboardBuilder':
        """Performs the barcode operation for the utility client.

Args:
    text: Text content supplied to the operation.
    button_id: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the barcode operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            button_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``'KeyboardBuilder'``).\n        "
        return self._rubika('Barcode', text, button_id=button_id)

    def reply_button(self, text: str, *, request_contact: bool=False, request_location: bool=False) -> 'KeyboardBuilder':
        """Performs the reply button operation for the utility client.

Args:
    text: Text content supplied to the operation.
    request_contact: Value used by this operation.
    request_location: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the reply_button operation.\n                \n                Args:\n                    text: Value of the declared parameter type.\n                    request_contact: Value of the declared parameter type.\n                    request_location: Value of the declared parameter type.\n                \n                \n                Returns:\n                    The operation result (``'KeyboardBuilder'``).\n                \n        \n        Raises:\n            KeyboardBuildError: Raised when the operation cannot complete.\n        "
        if request_contact and request_location:
            raise KeyboardBuildError('a reply button cannot request contact and location at the same time')
        self._require_text(text)
        self._rows[-1].append(_ButtonSpec(text=text, kind='Reply', payload={'request_contact': request_contact, 'request_location': request_location}))
        return self

    def build(self, target: str | PlatformCapabilities) -> object:
        """Performs the build operation for the utility client.

Args:
    target: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        'Executes the build operation.\n                \n                Args:\n                    target: Value of the declared parameter type.\n                \n                \n                Returns:\n                    The operation result (``object``).\n                \n        \n        Raises:\n            KeyboardBuildError: Raised when the operation cannot complete.\n        '
        platform, capabilities = _normalize_target(target)
        rows = [row for row in self._rows if row]
        if not rows:
            raise KeyboardBuildError('keyboard must contain at least one button')
        for row in rows:
            for spec in row:
                self._validate_spec(spec, platform, capabilities)
        if platform in {'telegram', 'bale'}:
            if any((spec.kind == 'Reply' for row in rows for spec in row)):
                return self._build_reply(rows, platform)
            if any((spec.kind in _RUBIKA_TYPES - {'Link'} for row in rows for spec in row)):
                raise KeyboardBuildError('Rubika-specific button types cannot be rendered for Telegram/Bale')
            return self._build_inline(rows, platform)
        if platform == 'rubika':
            return self._build_rubika(rows)
        raise KeyboardBuildError('custom capabilities require a known platform renderer')

    @staticmethod
    def _require_text(text: str) -> None:
        if not isinstance(text, str) or not text:
            raise KeyboardBuildError('button text cannot be empty')

    @staticmethod
    def _validate_spec(spec: _ButtonSpec, platform: str, capabilities: PlatformCapabilities) -> None:
        if spec.kind in _RUBIKA_TYPES - {'Link'} and platform != 'rubika':
            raise KeyboardBuildError(f'{spec.kind} is Rubika-only and cannot be rendered for {platform}')
        if spec.callback_data is not None and capabilities.callback_data_max_bytes is not None:
            encoded = len(spec.callback_data.encode('utf-8'))
            limit = capabilities.callback_data_max_bytes
            if encoded < 1 or encoded > limit:
                raise KeyboardBuildError(f'callback_data must be 1-{limit} bytes (UTF-8 encoded); got {encoded} bytes for {platform}')

    @staticmethod
    def _build_inline(rows: list[list[_ButtonSpec]], platform: str) -> object:
        if platform == 'telegram':
            from peyk.platforms.telegram.types import InlineKeyboardButton, InlineKeyboardMarkup
        else:
            from peyk.platforms.bale.types import InlineKeyboardButton, InlineKeyboardMarkup
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=s.text, callback_data=s.callback_data, url=s.url) for s in row] for row in rows])

    @staticmethod
    def _build_reply(rows: list[list[_ButtonSpec]], platform: str) -> object:
        if platform == 'telegram':
            from peyk.platforms.telegram.types import KeyboardButton, ReplyKeyboardMarkup
        else:
            from peyk.platforms.bale.types import KeyboardButton, ReplyKeyboardMarkup
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=s.text, request_contact=(s.payload or {}).get('request_contact'), request_location=(s.payload or {}).get('request_location')) for s in row] for row in rows])

    @staticmethod
    def _build_rubika(rows: list[list[_ButtonSpec]]) -> object:
        from peyk.platforms.rubika.types import Button, ButtonCalendar, ButtonLocation, ButtonNumberPicker, ButtonSelection, ButtonSelectionItem, ButtonStringPicker, ButtonTextbox, Keypad, KeypadRow
        result_rows = []
        for row in rows:
            result_buttons = []
            for spec in row:
                payload = dict(spec.payload or {})
                nested = None
                field_name = None
                if spec.kind == 'Selection':
                    payload['items'] = [ButtonSelectionItem(**item) if isinstance(item, dict) else item for item in payload.get('items', [])]
                    nested, field_name = (ButtonSelection(**payload), 'button_selection')
                elif spec.kind == 'Calendar':
                    nested, field_name = (ButtonCalendar(**payload), 'button_calendar')
                elif spec.kind == 'NumberPicker':
                    nested, field_name = (ButtonNumberPicker(**payload), 'button_number_picker')
                elif spec.kind == 'StringPicker':
                    nested, field_name = (ButtonStringPicker(**payload), 'button_string_picker')
                elif spec.kind == 'Location':
                    for key in ('default_pointer_location', 'default_map_location'):
                        if isinstance(payload.get(key), dict):
                            from peyk.platforms.rubika.types import Location
                            payload[key] = Location(**payload[key])
                    nested, field_name = (ButtonLocation(**payload), 'button_location')
                elif spec.kind == 'Textbox':
                    nested, field_name = (ButtonTextbox(**payload), 'button_textbox')
                kwargs: dict[str, object] = {'id': spec.callback_data or spec.url or spec.text, 'type': spec.kind, 'button_text': spec.text}
                if field_name:
                    kwargs[field_name] = nested
                result_buttons.append(Button(**kwargs))
            result_rows.append(KeypadRow(buttons=result_buttons))
        return Keypad(rows=result_rows)
__all__ = ['KeyboardBuilder', 'KeyboardBuildError']
