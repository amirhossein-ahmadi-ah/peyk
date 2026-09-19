"""Audited cross-platform capability registry."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Sequence

from peyk.platform_core.enums import PlatformName


class Feature(str, Enum):
    """Cross-platform features audited by Phase 1."""

    # Messaging
    TEXT = "messaging.text"
    PHOTO = "messaging.photo"
    VIDEO = "messaging.video"
    AUDIO = "messaging.audio"
    VOICE = "messaging.voice"
    DOCUMENT = "messaging.document"
    ANIMATION = "messaging.animation"
    STICKER = "messaging.sticker"
    CONTACT = "messaging.contact"
    LOCATION = "messaging.location"
    VENUE = "messaging.venue"
    POLL = "messaging.poll"
    DICE = "messaging.dice"
    MEDIA_GROUP = "messaging.media_group"
    COPY = "messaging.copy"
    FORWARD = "messaging.forward"
    EDIT_TEXT = "messaging.edit_text"
    EDIT_CAPTION = "messaging.edit_caption"
    EDIT_MEDIA = "messaging.edit_media"
    EDIT_MARKUP = "messaging.edit_markup"
    DELETE = "messaging.delete"
    BULK_DELETE = "messaging.bulk_delete"
    REPLY_TO = "messaging.reply_to"
    CHAT_ACTIONS = "messaging.chat_actions"
    REACTIONS = "messaging.reactions"
    LINK_PREVIEW_CONTROL = "messaging.link_preview_control"
    PROTECT_CONTENT = "messaging.protect_content"
    ENTITIES_FORMATTING = "messaging.entities_formatting"

    # Keyboards
    INLINE_KEYBOARD = "keyboards.inline"
    REPLY_KEYBOARD = "keyboards.reply"
    REMOVE_REPLY = "keyboards.remove_reply"
    FORCE_REPLY = "keyboards.force_reply"
    BUTTON_URL = "keyboards.button.url"
    BUTTON_CALLBACK = "keyboards.button.callback"
    BUTTON_WEB_APP = "keyboards.button.web_app"
    BUTTON_COPY_TEXT = "keyboards.button.copy_text"
    BUTTON_COLOR_STYLE = "keyboards.button.color_style"
    BUTTON_ICON_EMOJI = "keyboards.button.icon_emoji"
    BUTTON_REQUEST_CONTACT = "keyboards.button.request_contact"
    BUTTON_REQUEST_LOCATION = "keyboards.button.request_location"
    BUTTON_REQUEST_POLL = "keyboards.button.request_poll"
    BUTTON_REQUEST_USERS = "keyboards.button.request_users"
    BUTTON_REQUEST_CHAT = "keyboards.button.request_chat"
    BUTTON_PAY = "keyboards.button.pay"
    BUTTON_SWITCH_INLINE = "keyboards.button.switch_inline"
    BUTTON_LOGIN_URL = "keyboards.button.login_url"
    RUBIKA_BUTTON_SELECTION = "keyboards.rubika.selection"
    RUBIKA_BUTTON_CALENDAR = "keyboards.rubika.calendar"
    RUBIKA_BUTTON_NUMBER_PICKER = "keyboards.rubika.number_picker"
    RUBIKA_BUTTON_STRING_PICKER = "keyboards.rubika.string_picker"
    RUBIKA_BUTTON_LOCATION = "keyboards.rubika.location"
    RUBIKA_BUTTON_CAMERA_IMAGE = "keyboards.rubika.camera_image"
    RUBIKA_BUTTON_CAMERA_VIDEO = "keyboards.rubika.camera_video"
    RUBIKA_BUTTON_GALLERY_IMAGE = "keyboards.rubika.gallery_image"
    RUBIKA_BUTTON_GALLERY_VIDEO = "keyboards.rubika.gallery_video"
    RUBIKA_BUTTON_FILE = "keyboards.rubika.file"
    RUBIKA_BUTTON_AUDIO = "keyboards.rubika.audio"
    RUBIKA_BUTTON_RECORD_AUDIO = "keyboards.rubika.record_audio"
    RUBIKA_BUTTON_TEXTBOX = "keyboards.rubika.textbox"
    RUBIKA_BUTTON_LINK = "keyboards.rubika.link"
    RUBIKA_BUTTON_PHONE = "keyboards.rubika.ask_my_phone_number"
    RUBIKA_BUTTON_USER_LOCATION = "keyboards.rubika.ask_my_location"
    RUBIKA_BUTTON_BARCODE = "keyboards.rubika.barcode"

    # Callbacks
    CALLBACK_ANSWER = "callbacks.answer"
    CALLBACK_ALERT_TOAST = "callbacks.alert_toast"
    CALLBACK_DATA_LIMIT = "callbacks.data_byte_limit"

    # Updates
    POLLING = "updates.polling"
    WEBHOOK = "updates.webhook"
    WEBHOOK_SECRET_HEADER = "updates.webhook_secret_header"
    UPDATE_OFFSET = "updates.offset_kind"
    ALLOWED_UPDATES = "updates.allowed_updates"
    LONG_POLL_TIMEOUT = "updates.long_poll_timeout"

    # Chat administration
    BAN = "chat_admin.ban"
    UNBAN = "chat_admin.unban"
    RESTRICT = "chat_admin.restrict"
    PROMOTE = "chat_admin.promote"
    PIN = "chat_admin.pin"
    UNPIN = "chat_admin.unpin"
    INVITE_LINKS = "chat_admin.invite_links"
    MEMBER_COUNT = "chat_admin.member_count"
    ADMINISTRATORS = "chat_admin.administrators"
    PERMISSIONS = "chat_admin.permissions"
    TITLE = "chat_admin.title"
    DESCRIPTION = "chat_admin.description"
    CHAT_PHOTO = "chat_admin.photo"
    LEAVE = "chat_admin.leave"
    JOIN_REQUESTS = "chat_admin.join_requests"
    FORUM_TOPICS = "chat_admin.forum_topics"
    MEMBER_STATUS_UPDATES = "chat_admin.member_status_updates"

    # Files
    GET_FILE = "files.get_file"
    UPLOAD_BYTES = "files.upload_bytes"
    MULTI_STEP_UPLOAD = "files.multi_step_upload"

    # Payments/profile/inline
    PAYMENTS = "payments"
    BOT_COMMANDS = "bot_profile.commands"
    BOT_NAME = "bot_profile.name"
    BOT_DESCRIPTION = "bot_profile.description"
    INLINE_MODE = "inline_mode"

    # Telegram-only
    TELEGRAM_GAMES = "telegram.games"
    TELEGRAM_PASSPORT = "telegram.passport"
    TELEGRAM_BUSINESS = "telegram.business"
    TELEGRAM_STORIES = "telegram.stories"
    TELEGRAM_GIFTS = "telegram.gifts"
    TELEGRAM_STARS = "telegram.stars"


class SupportLevel(str, Enum):
    """Degree of implementation support established by the audit."""

    FULL = "full"
    PARTIAL = "partial"
    EMULATED = "emulated"
    NONE = "none"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Support:
    """Audited support for one feature on one platform."""

    level: SupportLevel
    evidence: tuple[tuple[str, str], ...] = ()
    limits: Mapping[str, object] = field(default_factory=dict)
    note: str = ""
    confidence: str = "confirmed"

    def limit(self, name: str) -> object | None:
        """Return an audited limit, or ``None`` when it is not recorded."""
        return self.limits.get(name)


Platform = str


@dataclass(frozen=True)
class CapabilitySet:
    """Capabilities for one platform."""

    platform: Platform
    features: Mapping[Feature, Support]

    def supports(self, feature: Feature) -> bool:
        """Return whether support is established as usable rather than unknown."""
        support = self.get(feature)
        return support.level in {SupportLevel.FULL, SupportLevel.PARTIAL, SupportLevel.EMULATED}

    def get(self, feature: Feature) -> Support:
        """Return the audited support record for ``feature``."""
        return self.features.get(feature, Support(SupportLevel.UNKNOWN, confidence="low", note="Not audited."))

    def limit(self, name: str) -> object | None:
        """Return a named limit from any feature record that declares it."""
        for support in self.features.values():
            value = support.limit(name)
            if value is not None:
                return value
        return None


@dataclass(frozen=True)
class CapabilityMatrix:
    """Complete three-state matrix and comparison helpers."""

    platforms: Mapping[Platform, CapabilitySet]

    def for_platform(self, platform: Platform) -> CapabilitySet:
        """Return the capability set for a platform identifier."""
        return self.platforms[platform]

    def missing_on(self, platform: Platform) -> tuple[Feature, ...]:
        """Return features audited as unsupported on ``platform``."""
        return tuple(f for f, s in self.for_platform(platform).features.items() if s.level is SupportLevel.NONE)

    def diff(self, a: Platform, b: Platform) -> Mapping[Feature, tuple[Support, Support]]:
        """Return features whose audited support differs between two platforms."""
        left, right = self.for_platform(a), self.for_platform(b)
        return MappingProxyType({
            feature: (left.get(feature), right.get(feature))
            for feature in Feature
            if left.get(feature) != right.get(feature)
        })


def get_capabilities(platform: Platform | PlatformName) -> CapabilitySet:
    """Return the audited capabilities for ``platform``."""
    return CAPABILITY_MATRIX.for_platform(platform.value if isinstance(platform, PlatformName) else platform)


# Imported after the public types so platform declaration modules can use them.
from . import bale, rubika, telegram  # noqa: E402

CAPABILITY_MATRIX = CapabilityMatrix(MappingProxyType({
    "telegram": CapabilitySet("telegram", telegram.CAPABILITIES),
    "bale": CapabilitySet("bale", bale.CAPABILITIES),
    "rubika": CapabilitySet("rubika", rubika.CAPABILITIES),
}))

PLATFORM_SPECIFIC_METHODS: Mapping[str, tuple[str, ...]] = MappingProxyType({
    "telegram": telegram.PLATFORM_SPECIFIC_METHODS,
    "bale": bale.PLATFORM_SPECIFIC_METHODS,
    "rubika": rubika.PLATFORM_SPECIFIC_METHODS,
})

__all__ = [
    "CapabilityMatrix", "CapabilitySet", "Feature", "PLATFORM_SPECIFIC_METHODS",
    "Support", "SupportLevel", "get_capabilities", "CAPABILITY_MATRIX",
]
