Keyboards
=========

Use neutral builders and let the bot render them for its selected platform.

.. code-block:: python

   from peyk import Bot
   from peyk.keyboard import InlineKeyboardBuilder, ButtonStyle

   bot = Bot("TOKEN", platform="telegram")
   keyboard = (InlineKeyboardBuilder()
               .button(text="Open", url="https://example.com")
               .button(text="Save", callback_data="save", style=ButtonStyle.SUCCESS)
               .adjust(1)
               .as_markup())

   @bot.command("start")
   async def start(message):
       await message.answer("Choose:", reply_markup=keyboard)

Platform notes
--------------

+----------------------+----------+------+--------+
| Surface              | Telegram | Bale | Rubika |
+======================+==========+======+========+
| Inline keyboards     | yes      | yes  | yes    |
+----------------------+----------+------+--------+
| Reply keyboards      | yes      | yes  | yes    |
+----------------------+----------+------+--------+
| Color style          | yes*     | no   | unknown|
+----------------------+----------+------+--------+
| Rubika native kinds  | no       | no   | yes    |
+----------------------+----------+------+--------+

``*`` Telegram style values are represented in the audited type surface; the wire values remain an evidence-qualified area in the capability registry.
