from collections.abc import Awaitable, Callable
from typing import assert_type

from peyk import Bot, F
from peyk.types import Message

bot = Bot("TOKEN", platform="telegram")

@bot.message(F.text == "hi")
async def decorated(message: Message) -> str:
    return "ok"

assert_type(decorated, Callable[[Message], Awaitable[str]])
