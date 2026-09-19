Routers and handlers
====================

Use :class:`peyk.Router` to group handlers and filters. Router dispatch is ordered and first-match: once a handler handles an event, later handlers and child routers are not selected for that event.

.. code-block:: python

   from peyk import Bot, Router, F

   bot = Bot("TOKEN", platform="telegram")
   router = Router(name="messages")

   @router.message(F.text)
   async def echo(message):
       await message.answer(message.text or "")

   bot.include_router(router)

The simple ``@bot.message`` and ``@bot.command`` forms register on the bot's built-in router.

``Router`` and ``Dispatcher`` have the same ``command`` shorthand, so a command handler
does not need to be attached to a bot:

.. code-block:: python

   admin = Router(name="admin")

   @admin.command("admin")
   async def admin_command(message):
       await message.answer("Admin router handled /admin")

   # Routers are tried in the order they are included and the first match wins.
   # Include specific routers before catch-all ones (such as ``F.text`` echo).
   dispatcher.include_router(admin)
   dispatcher.include_router(router)
