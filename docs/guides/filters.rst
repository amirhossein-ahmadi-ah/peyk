Filters
=======

Peyk exposes ``F``, ``Command``, ``CommandStart`` and ``CallbackData`` from ``peyk.filters`` and the package root. Filters may return a boolean or a mapping that is injected into the handler.

.. code-block:: python

   from peyk import Bot, F, CommandStart

   bot = Bot("TOKEN", platform="telegram")

   @bot.message(CommandStart())
   async def start(message, command):
       await message.answer(f"command={command.command}")

   @bot.message(F.text)
   async def text(message):
       await message.answer(message.text or "")

Filters can be combined with ``&``, ``|`` and ``~``.
