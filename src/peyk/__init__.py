"""Peyk public API."""
import asyncio

from .bot import BaleBot, Bot, BotDefaults, BotNotBoundError, InvalidTokenError, RubikaBot, TelegramBot, UnsupportedPolicy, StyleFallback
from .bot.base import ClientLifecycle
from .types import CallbackQuery, Chat, ChatMember, ChatType, ContentType, File, Message, User
from .enums import ChatAction, ParseMode, Platform, ButtonStyle
from .platform_core.capabilities import Feature
from .dispatcher import Dispatcher, Router, ErrorEvent, SkipHandler, UNHANDLED
from .flags import flags, get_flag, check_flags
from .filters import F, CallbackData, Command, CommandObject, CommandStart, ChatTypeFilter, MagicData, PlatformFilter, StateFilter, SupportsFilter

def run(*bots: Bot[ClientLifecycle], **polling_options: object) -> None:
    """Run several bots concurrently with independent routers."""
    asyncio.run(_run_bots(bots, polling_options))


async def _run_bots(bots: tuple[Bot[ClientLifecycle], ...], polling_options: dict[str, object]) -> None:
    if not bots:
        raise ValueError("run() requires at least one bot")
    await asyncio.gather(*(bot.run_async(**polling_options) for bot in bots))


__version__ = "1.0.0"

__all__ = [
    "BaleBot", "Bot", "Dispatcher", "F", "Command", "CommandStart", "CommandObject", "CallbackData", "ChatTypeFilter", "StateFilter", "MagicData", "PlatformFilter", "SupportsFilter", "SkipHandler", "UNHANDLED", "ErrorEvent", "BotDefaults", "BotNotBoundError", "InvalidTokenError", "run", "CallbackQuery",
    "Chat", "ChatMember", "ChatType", "ContentType", "Feature", "File", "Message", "RubikaBot", "Router",
    "TelegramBot", "flags", "get_flag", "check_flags", "UnsupportedPolicy", "StyleFallback", "User", "ChatAction", "ParseMode", "Platform", "ButtonStyle",
]
