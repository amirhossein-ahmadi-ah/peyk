Webhook
=======

The built-in aiohttp webhook runner supports Telegram, Bale and Rubika through the audited registrar contracts.

.. code-block:: python

   from peyk import Bot, Dispatcher

   bot = Bot("TOKEN", platform="telegram")
   dp = Dispatcher()
   dp.include_router(bot.router)

   if __name__ == "__main__":
       dp.run_webhook(bot, base_url="https://example.com", secrets=["change-me"] )

Telegram supports its platform secret header. Bale and Rubika use the framework path secret because no platform secret-header contract is documented in the project evidence.
