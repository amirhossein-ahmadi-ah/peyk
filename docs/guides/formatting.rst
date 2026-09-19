Formatting
==========

``RichText`` is composed independently of the target platform. ``Bot.send_message`` resolves it using the active platform capabilities.

.. code-block:: python

   from peyk import Bot
   from peyk.formatting import Text

   bot = Bot("TOKEN", platform="telegram")

   @bot.command("hello")
   async def hello(message):
       text = Text("Hello ").bold("developer").line().link("docs", "https://example.com")
       await message.answer(text)

When a formatting feature is unsupported, the configured ``UnsupportedPolicy`` controls whether it raises, strips the unsupported part, or degrades with a warning.
