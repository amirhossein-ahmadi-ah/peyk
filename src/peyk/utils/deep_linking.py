from __future__ import annotations
import base64
from urllib.parse import quote
from peyk.platform_core.errors import UnsupportedFeatureError
from peyk.platform_core.capabilities import Feature

def encode_payload(payload: str | bytes) -> str:
    """Encode UTF-8 payload using unpadded URL-safe base64."""
    raw = payload.encode() if isinstance(payload, str) else payload
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")
def decode_payload(payload: str) -> str:
    """Decode an unpadded URL-safe base64 payload as UTF-8."""
    return base64.urlsafe_b64decode((payload + "=" * (-len(payload) % 4)).encode()).decode()
async def create_start_link(bot: object, payload: str | bytes) -> str:
    """Create the confirmed Telegram Bot API ``start`` deep link."""
    if getattr(bot, "platform", None) != "telegram": raise UnsupportedFeatureError(Feature.BOT_COMMANDS, str(getattr(bot, "platform", "unknown")), None)
    me = await bot.me(); username = getattr(me, "username", None) or getattr(getattr(me, "raw", None), "username", None)
    if not username: raise UnsupportedFeatureError(Feature.BOT_COMMANDS, "telegram", None)
    return f"https://t.me/{username}?start={quote(encode_payload(payload), safe='_-')}"
