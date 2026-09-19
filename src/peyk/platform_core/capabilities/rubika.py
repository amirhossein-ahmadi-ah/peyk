"""Rubika capability declarations derived from the audited official-contract implementation."""
from __future__ import annotations
from . import Feature, Support, SupportLevel
from ._common import s

def _base() -> dict[Feature, Support]:
    return {f: Support(SupportLevel.UNKNOWN, confidence="low", note="Not independently established by the Phase 1 audit.") for f in Feature}
CAPABILITIES = _base()
for feature, method in {
    Feature.TEXT:"RubikaClient.send_message", Feature.CONTACT:"RubikaClient.send_contact", Feature.LOCATION:"RubikaClient.send_location",
    Feature.POLL:"RubikaClient.send_poll", Feature.FORWARD:"RubikaClient.forward_message", Feature.EDIT_TEXT:"RubikaClient.edit_message_text",
    Feature.EDIT_MARKUP:"RubikaClient.edit_message_keypad", Feature.DELETE:"RubikaClient.delete_message", Feature.REPLY_TO:"RubikaClient.send_message",
    Feature.GET_FILE:"RubikaClient.get_file", Feature.POLLING:"RubikaClient.get_updates", Feature.BOT_COMMANDS:"RubikaClient.set_commands",
    Feature.BAN:"RubikaClient.ban_chat_member", Feature.UNBAN:"RubikaClient.unban_chat_member", Feature.LEAVE:"docs/decisions.md",
    Feature.INLINE_KEYBOARD:"rubika.Button.button_text", Feature.REPLY_KEYBOARD:"rubika.Button.button_text", Feature.REMOVE_REPLY:"RubikaClient.remove_chat_keypad",
}.items(): CAPABILITIES[feature] = s(SupportLevel.FULL, method)
for f, note in {
    Feature.PHOTO:"requestSendFile -> upload -> sendFile is the confirmed three-step flow.", Feature.VIDEO:"requestSendFile -> upload -> sendFile is the confirmed three-step flow.",
    Feature.DOCUMENT:"requestSendFile -> upload -> sendFile is the confirmed three-step flow.", Feature.VOICE:"requestSendFile -> upload -> sendFile is the confirmed three-step flow.",
}.items(): CAPABILITIES[f] = s(SupportLevel.EMULATED, "RubikaClient.upload_and_send_file", note=note)
CAPABILITIES[Feature.UPLOAD_BYTES] = s(SupportLevel.FULL, "RubikaClient.upload_file")
CAPABILITIES[Feature.MULTI_STEP_UPLOAD] = s(SupportLevel.FULL, "RubikaClient.request_send_file", "RubikaClient.upload_file", "RubikaClient.send_file")
CAPABILITIES[Feature.ENTITIES_FORMATTING] = s(SupportLevel.PARTIAL, "rubika.MetadataPart.type", note="D5 confirms structured metadata formatting rather than a Telegram parse mode; formatted edit metadata is NONE/inferred because editMessageText has no metadata parameter.")
CAPABILITIES[Feature.CALLBACK_DATA_LIMIT] = s(SupportLevel.UNKNOWN, "docs/decisions.md", note="button_id is confirmed but no callback-data byte limit is established.", confidence="low")
CAPABILITIES[Feature.CALLBACK_ANSWER] = s(SupportLevel.UNKNOWN, "docs/decisions.md", note="No confirmed callback-answer method in the audited Rubika client.", confidence="low")
CAPABILITIES[Feature.UPDATE_OFFSET] = s(SupportLevel.FULL, "RubikaClient.get_updates", offset_kind="offset_id")
CAPABILITIES[Feature.ALLOWED_UPDATES] = s(SupportLevel.UNKNOWN, "RubikaClient.update_bot_endpoints", note="Endpoint/update parameters remain a documented UNKNOWN area.", confidence="low")
CAPABILITIES[Feature.LONG_POLL_TIMEOUT] = s(SupportLevel.UNKNOWN, "RubikaClient.get_updates", note="The audited method exposes no timeout parameter.", confidence="low")
CAPABILITIES[Feature.WEBHOOK] = s(SupportLevel.PARTIAL, "RubikaClient.update_bot_endpoints", note="Endpoint method is implemented; updateBotEndpoints parameter semantics remain UNKNOWN per R6.", confidence="low")
for f, field in {Feature.RUBIKA_BUTTON_SELECTION:"button_selection", Feature.RUBIKA_BUTTON_CALENDAR:"button_calendar", Feature.RUBIKA_BUTTON_NUMBER_PICKER:"button_number_picker", Feature.RUBIKA_BUTTON_STRING_PICKER:"button_string_picker", Feature.RUBIKA_BUTTON_LOCATION:"button_location", Feature.RUBIKA_BUTTON_TEXTBOX:"button_textbox"}.items():
    CAPABILITIES[f] = s(SupportLevel.FULL, f"rubika.Button.{field}")
for f in (Feature.RUBIKA_BUTTON_CAMERA_IMAGE, Feature.RUBIKA_BUTTON_CAMERA_VIDEO, Feature.RUBIKA_BUTTON_GALLERY_IMAGE, Feature.RUBIKA_BUTTON_GALLERY_VIDEO, Feature.RUBIKA_BUTTON_FILE, Feature.RUBIKA_BUTTON_AUDIO, Feature.RUBIKA_BUTTON_RECORD_AUDIO, Feature.RUBIKA_BUTTON_LINK, Feature.RUBIKA_BUTTON_PHONE, Feature.RUBIKA_BUTTON_USER_LOCATION, Feature.RUBIKA_BUTTON_BARCODE):
    CAPABILITIES[f] = s(SupportLevel.FULL, "docs/decisions.md", note="Button kind is represented by the audited Rubika enum/model set.")
for f in (Feature.TELEGRAM_GAMES, Feature.TELEGRAM_PASSPORT, Feature.TELEGRAM_BUSINESS, Feature.TELEGRAM_STORIES, Feature.TELEGRAM_GIFTS, Feature.TELEGRAM_STARS):
    CAPABILITIES[f] = s(SupportLevel.NONE, "docs/decisions.md", note="This feature is classified as Telegram-only by the Phase 1 specification.", confidence="inferred")
PLATFORM_SPECIFIC_METHODS = ('close', 'edit_chat_keypad', 'get_chat', 'get_me', 'field:Button.id', 'field:Button.type', 'field:Button.button_text', 'field:ButtonSelection.selection_id', 'field:ButtonSelection.search_type', 'field:ButtonSelection.get_type', 'field:ButtonSelection.items', 'field:ButtonSelection.is_multi_selection', 'field:ButtonSelection.columns_count', 'field:ButtonSelection.title', 'field:ButtonCalendar.default_value', 'field:ButtonCalendar.type', 'field:ButtonCalendar.min_year', 'field:ButtonCalendar.max_year', 'field:ButtonCalendar.title', 'field:ButtonNumberPicker.min_value', 'field:ButtonNumberPicker.max_value', 'field:ButtonNumberPicker.default_value', 'field:ButtonNumberPicker.title', 'field:ButtonStringPicker.items', 'field:ButtonStringPicker.default_value', 'field:ButtonStringPicker.title', 'field:ButtonLocation.default_pointer_location', 'field:ButtonLocation.default_map_location', 'field:ButtonLocation.type', 'field:ButtonLocation.title', 'field:ButtonTextbox.type_line', 'field:ButtonTextbox.type_keypad', 'field:ButtonTextbox.place_holder', 'field:ButtonTextbox.title', 'field:ButtonTextbox.default_value', 'field:Button.button_calendar', 'field:Button.button_location', 'field:Button.button_number_picker', 'field:Button.button_selection', 'field:Button.button_string_picker', 'field:Button.button_textbox')

CAPABILITIES[Feature.WEBHOOK_SECRET_HEADER] = s(SupportLevel.NONE, "docs/decisions.md", note="Rubika webhook_security.py states that the documented webhook contract has no request signing or shared-secret header.", confidence="confirmed")
CAPABILITIES[Feature.CHAT_ACTIONS] = s(SupportLevel.NONE, "docs/decisions.md", note="No Rubika chat-action method is present in the audited official-contract client.", confidence="confirmed")
CAPABILITIES[Feature.CALLBACK_ANSWER] = s(SupportLevel.NONE, "docs/decisions.md", note="Rubika callback events have no callback-query identifier in the audited model, so automatic callback acknowledgement is not available.", confidence="confirmed")
CAPABILITIES[Feature.MEDIA_GROUP] = s(SupportLevel.NONE, "docs/decisions.md", note="No Rubika send-media-group operation is present in the audited official-contract client.", confidence="confirmed")
