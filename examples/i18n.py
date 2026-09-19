"""Gettext-backed translation middleware example."""
from pathlib import Path
from peyk import Bot
from peyk.utils import I18n, I18nMiddleware

i18n = I18n(Path(__file__).parent / "locales", default_locale="en")
bot = Bot("TOKEN", platform="telegram")
bot.router.handler_middleware(I18nMiddleware(i18n))

@bot.command("start")
async def start(message, gettext):
    await message.answer(gettext("Hello"))

if __name__ == "__main__":
    bot.run()
