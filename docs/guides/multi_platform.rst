Writing multi-platform bots
==========================

Create one ``Bot`` per platform and keep application handlers platform-neutral. The platform is selected once at construction time.

.. code-block:: python

   from peyk import Bot, run

   telegram = Bot("TELEGRAM_TOKEN", platform="telegram")
   bale = Bot("BALE_TOKEN", platform="bale")

   @telegram.command("start")
   @bale.command("start")
   async def start(message):
       await message.answer("Hello")

   if __name__ == "__main__":
       run(telegram, bale)

Policies
--------

Capability checks are available through ``bot.supports(feature)``. Unsupported operations either raise or degrade according to the bot's configured policy. Do not infer support from another platform; use the audited capability matrix.

Fallbacks
---------

Neutral keyboards and formatting are resolved at send time. Platform-specific features should be guarded with a capability check or kept behind a platform-specific branch at the application boundary.

Bale authentication errors
---------------------------

A ``403 Forbidden`` from ``https://tapi.bale.ai/bot<TOKEN>/...`` is returned by
Bale before Peyk can parse a successful API response.  Check that the bot token
is current and that the bot is allowed to send to the target chat.  Do not
commit bot tokens to logs, examples, or source control; rotate a token if it
has been exposed.
