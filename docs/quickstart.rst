Quickstart
==========

Simple bot
----------

Start with the small API when one bot and one router are enough:

.. code-block:: python

   from peyk import Bot

   bot = Bot("TOKEN", platform="bale")

   @bot.command("start")
   async def start(message):
       await message.answer("Hello!")

   bot.run()

The same code works with ``platform="telegram"`` or ``platform="rubika"``.
Async handlers are recommended, although the router also accepts synchronous
handlers. ``bot.run()`` is blocking; use ``await bot.run_async()`` when an
application already owns the event loop.

Explicit Dispatcher
--------------------

For larger applications, the bot's plain router can be included in an
explicit dispatcher:

.. code-block:: python

   from peyk import Bot, Dispatcher

   bot = Bot("TOKEN", platform="telegram")
   dp = Dispatcher()
   dp.include_router(bot.router)

   @bot.command("start")
   async def start(message):
       await message.answer("Hello!")

   dp.run_polling(bot)

The dispatcher API is useful when several routers or explicit workflow data
need to be managed together.

Webhook adapter example
-----------------------

The webhook core is independent of aiohttp. A FastAPI/Starlette adapter can
read the request body and headers, call ``WebhookProcessor.handle(bot, body,
headers)``, and translate ``WebhookResult.status``/``body`` into the framework's
response type. No FastAPI or Starlette dependency is required by Peyk.

For a stable externally registered URL, pass a stable webhook ``secret`` to
``dp.run_webhook(..., secrets=[...])``. If it is omitted, Peyk generates a
cryptographically random path secret; that URL must be re-registered after a
restart. Telegram also receives the same supplied/generated value as its
``secret_token`` header secret. Bale and Rubika have no confirmed platform
secret-header mechanism, so their protection is the secret path (plus an
optional IP filter when using ``SimpleRequestHandler``).
