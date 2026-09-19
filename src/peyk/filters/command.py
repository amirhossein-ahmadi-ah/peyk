from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern

from .base import BaseFilter
from peyk.platform_core.contracts import IncomingMessage


@dataclass(frozen=True)
class CommandObject:
    """Parsed command information supplied to a matching handler."""
    prefix: str
    command: str
    mention: str | None = None
    args: str | None = None
    regexp_match: re.Match[str] | None = None
    magic_result: object | None = None


class Command(BaseFilter):
    """Match a command and expose its parsed ``CommandObject`` as ``command``."""

    def __init__(self, *values: str, prefix: str = "/", ignore_case: bool = False,
                 ignore_mention: bool = False, magic: object | None = None) -> None:
        if not values:
            raise ValueError("Command requires at least one command name")
        if not prefix or any(ch.isspace() for ch in prefix):
            raise ValueError("command prefix must be a non-empty token")
        self.values = tuple(v[ len(prefix):] if v.startswith(prefix) else v for v in values)
        if any(not v or any(ch.isspace() for ch in v) for v in self.values):
            raise ValueError("command name must be a non-empty token")
        self.prefix = prefix
        self.ignore_case = ignore_case
        self.ignore_mention = ignore_mention
        self.magic = magic
        flags = re.IGNORECASE if ignore_case else 0
        names = "|".join(re.escape(v) for v in self.values)
        self._pattern: Pattern[str] = re.compile(
            rf"^({re.escape(prefix)})({names})(?:@([A-Za-z0-9_]+))?(?:\s+(.*))?$", flags
        )

    async def __call__(self, event: object, **data: object) -> bool | dict[str, object]:
        if not isinstance(event, IncomingMessage) or not event.text:
            return False
        match = self._pattern.match(event.text)
        if match is None:
            return False
        mention = match.group(3)
        bot = data.get("bot")
        if mention and not self.ignore_mention:
            if bot is None or not hasattr(bot, "me"):
                return False
            me = await bot.me()  # type: ignore[no-any-return]
            username = getattr(me, "username", None)
            if not username or username.casefold() != mention.casefold():
                return False
        command = CommandObject(
            prefix=match.group(1), command=match.group(2), mention=mention,
            args=match.group(4), regexp_match=match,
        )
        if self.magic is not None:
            from .base import normalize_filter
            result = await normalize_filter(self.magic)(command, **data)
            if not result:
                return False
            if isinstance(result, dict):
                command = CommandObject(**{**command.__dict__, "magic_result": result})
        return {"command": command}


class CommandStart(Command):
    """Match the ``/start`` command, optionally requiring deep-link arguments."""

    def __init__(self, deep_link: bool = False, **kwargs: object) -> None:
        self.deep_link = deep_link
        super().__init__("start", **kwargs)

    async def __call__(self, event: object, **data: object) -> bool | dict[str, object]:
        result = await super().__call__(event, **data)
        if not result:
            return False
        command = result["command"]
        if not isinstance(command, CommandObject):
            return False
        if self.deep_link and not command.args:
            return False
        if not self.deep_link and command.args:
            # aiogram-compatible CommandStart accepts regular /start arguments too;
            # deep_link only controls the dedicated requirement.
            pass
        return result
