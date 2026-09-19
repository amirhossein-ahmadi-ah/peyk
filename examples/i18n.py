"""Gettext-backed translation: reply in each user's own language.

I18n = "internationalization": the bot keeps its texts in translation files
(``locales/<lang>/LC_MESSAGES/messages.po``, compiled to ``messages.mo``) and
answers in the language of the user who wrote to it. Users whose language has
no catalog (here: anything but Persian) simply get the original English text.
"""
from pathlib import Path
from peyk import Bot
from peyk.utils import I18n, I18nMiddleware

# Where the .mo files live, and the language used when the user's is unknown.
i18n = I18n(Path(__file__).parent / "locales", default_locale="en")
bot = Bot("TOKEN", platform="telegram")
# Picks the locale from the sender's Telegram language and injects
# ``gettext`` / ``ngettext`` / ``locale`` into every handler that asks for them.
bot.router.handler_middleware(I18nMiddleware(i18n))


@bot.command("start")
async def start(message, gettext, locale):
    await message.answer(gettext("Hello"))
    await message.answer(gettext("Your language is: %s") % locale)


if __name__ == "__main__":
    bot.run()
