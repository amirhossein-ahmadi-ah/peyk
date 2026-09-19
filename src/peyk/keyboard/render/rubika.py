from __future__ import annotations
from dataclasses import asdict
from peyk.keyboard.ir import InlineKeyboard, ReplyKeyboard, KeyboardRemove, ForceReply
from peyk.keyboard.rubika import _RubikaButton
from peyk.platform_core.capabilities import CapabilitySet, Feature
from peyk.bot.policy import UnsupportedPolicy, StyleFallback
KeyboardPolicy = UnsupportedPolicy | tuple[UnsupportedPolicy, StyleFallback]
from peyk.platforms.rubika.types import Button, Keypad, KeypadRow, ButtonSelection, ButtonSelectionItem, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonLocation, ButtonTextbox
_KIND = {'Selection': (Feature.RUBIKA_BUTTON_SELECTION, 'button_selection', ButtonSelection), 'Calendar': (Feature.RUBIKA_BUTTON_CALENDAR, 'button_calendar', ButtonCalendar), 'NumberPicker': (Feature.RUBIKA_BUTTON_NUMBER_PICKER, 'button_number_picker', ButtonNumberPicker), 'StringPicker': (Feature.RUBIKA_BUTTON_STRING_PICKER, 'button_string_picker', ButtonStringPicker), 'Location': (Feature.RUBIKA_BUTTON_LOCATION, 'button_location', ButtonLocation), 'Textbox': (Feature.RUBIKA_BUTTON_TEXTBOX, 'button_textbox', ButtonTextbox)}

def rubika_buttons(buttons: list[list[_RubikaButton]], capabilities: CapabilitySet) -> Keypad:
    """Performs the rubika buttons operation for the keyboard client.

Args:
    buttons: Value used by this operation.
    capabilities: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    rows = []
    for row in buttons:
        out = []
        for b in row:
            kind = type(b).__name__
            feature, field, cls = _KIND.get(kind, (getattr(Feature, f'RUBIKA_BUTTON_{kind.upper()}', Feature.RUBIKA_BUTTON_LINK), None, None))
            if not capabilities.supports(feature):
                raise ValueError(f'unsupported Rubika feature: {feature.value}')
            payload = {'id': b.button_id, 'type': kind, 'button_text': b.text}
            if field:
                d = asdict(b)
                d.pop('text', None)
                d.pop('button_id', None)
                if kind == 'Selection':
                    d['items'] = [ButtonSelectionItem(**x) if isinstance(x, dict) else x for x in d['items']]
                payload[field] = cls(**d)
            if kind == 'Link':
                payload['type'] = 'Link'
            out.append(Button(**payload))
        rows.append(KeypadRow(buttons=out))
    return Keypad(rows=rows)

def inline_keyboard(ir: InlineKeyboard, capabilities: CapabilitySet, policy: KeyboardPolicy) -> Keypad:
    """Performs the inline keyboard operation for the keyboard client.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    rows = []
    for row in ir.inline_keyboard:
        out = []
        for b in row:
            if not b.text:
                raise ValueError('button text cannot be empty')
            data = b.packed_callback_data() or b.url or b.text
            if b.callback_data is not None and capabilities.get(Feature.CALLBACK_DATA_LIMIT).limit('callback_data_max_bytes') is not None:
                raise ValueError('Rubika callback-data limit is UNKNOWN; no local byte limit is applied') if False else None
            out.append(Button(id=data, type='Simple', button_text=b.text))
        rows.append(KeypadRow(buttons=out))
    return Keypad(rows=rows)

def reply_keyboard(ir: ReplyKeyboard, capabilities: CapabilitySet, policy: KeyboardPolicy) -> dict[str, object]:
    """Performs the reply keyboard operation for the keyboard client.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    rows = []
    for row in ir.keyboard:
        out = []
        for b in row:
            if not b.text:
                raise ValueError('button text cannot be empty')
            if b.request_contact and (not capabilities.supports(Feature.BUTTON_REQUEST_CONTACT)):
                raise ValueError('unsupported request_contact')
            if b.request_location and (not capabilities.supports(Feature.BUTTON_REQUEST_LOCATION)):
                raise ValueError('unsupported request_location')
            out.append(Button(id=b.text, type='Simple', button_text=b.text))
        rows.append(KeypadRow(buttons=out))
    return {'chat_keypad': Keypad(rows=rows, resize_keyboard=ir.resize_keyboard, one_time_keyboard=ir.one_time_keyboard), 'chat_keypad_type': 'New'}

def remove_keyboard(ir: KeyboardRemove, capabilities: CapabilitySet, policy: KeyboardPolicy) -> dict[str, object]:
    """Removes keyboard through the keyboard API.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    return {'chat_keypad_type': 'Remove'}

def force_reply(ir: ForceReply, capabilities: CapabilitySet, policy: KeyboardPolicy) -> dict[str, object]:
    """Performs the force reply operation for the keyboard client.

Args:
    ir: Value used by this operation.
    capabilities: Value used by this operation.
    policy: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
    return {'chat_keypad_type': 'New'}
