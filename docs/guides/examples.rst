Complete examples
=================

The examples shipped with Peyk are intended to demonstrate a complete event
flow, not just an isolated handler. In particular, examples that depend on an
incoming event also show how the user can produce that event.

Callback queries
----------------

``examples/callback_data.py`` sends an inline keyboard containing packed
``CallbackData`` values and then receives and decodes the resulting callback
query:

.. code-block:: python

   from peyk import Bot, CallbackData
   from peyk.keyboard import InlineKeyboardBuilder

   class Product(CallbackData, prefix="product"):
       id: int
       action: str

   bot = Bot("TOKEN", platform="telegram")

   @bot.command("products")
   async def products(message):
       keyboard = (
           InlineKeyboardBuilder()
           .button(text="Buy", callback_data=Product(id=42, action="buy").pack())
           .button(text="Details", callback_data=Product(id=42, action="details").pack())
           .adjust(2)
           .as_markup()
       )
       await message.answer("Choose an action:", reply_markup=keyboard)

   @bot.callback_query(Product.filter())
   async def callback(query, callback_data: Product):
       await query.answer(f"{callback_data.action}: product #{callback_data.id}")

The important part is that the example has both halves: a handler that creates
the callback button and a handler that consumes the callback query.

Inline mode
-----------

``examples/inline_mode.py`` demonstrates the complete Telegram flow. The
``/inline`` command sends a button with ``switch_inline_query_current_chat``;
pressing it opens inline mode in the current chat. The inline-query handler
then returns a real ``InlineQueryResultArticle``.

.. code-block:: python

   from peyk import Bot
   from peyk.platforms.telegram.types import (
       InlineKeyboardButton,
       InlineKeyboardMarkup,
       InlineQueryResultArticle,
       InputTextMessageContent,
   )

   bot = Bot("TOKEN", platform="telegram")

   @bot.command("inline")
   async def open_inline_mode(message):
       keyboard = InlineKeyboardMarkup(inline_keyboard=[[
           InlineKeyboardButton(
               text="Search inline",
               switch_inline_query_current_chat="peyk",
           )
       ]])
       await message.answer("Press the button:", reply_markup=keyboard)

   @bot.router.inline_query()
   async def inline(query):
       text = query.query or "Peyk inline result"
       result = InlineQueryResultArticle(
           id="1",
           title=f"Echo: {text}",
           input_message_content=InputTextMessageContent(
               message_text=f"You selected: {text}"
           ),
       )
       await query.answer([result], cache_time=1, is_personal=True)

FSM
---

``examples/finite_state_machine.py`` is a real three-step event flow: ``/start``
sets ``Form.name``, the next message stores the name and moves to
``Form.age``, and the following message reads the saved data and clears the
conversation.

.. code-block:: python

   from peyk import Bot, Dispatcher
   from peyk.filters import StateFilter
   from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup

   class Form(StatesGroup):
       name = State()
       age = State()

   dp = Dispatcher(storage=MemoryStorage())
   bot = Bot("TOKEN", platform="telegram")

   @dp.command("start")
   async def start(message, state: FSMContext):
       await state.set_state(Form.name)
       await message.answer("What is your name?")

   @dp.message(StateFilter(Form.name))
   async def name_step(message, state: FSMContext):
       await state.update_data(name=message.text or "")
       await state.set_state(Form.age)
       await message.answer("How old are you?")

   @dp.message(StateFilter(Form.age))
   async def age_step(message, state: FSMContext):
       data = await state.update_data(age=message.text or "")
       await message.answer(f"Thanks {data['name']}! Your age is {data['age']}.")
       await state.clear()

   dp.run_polling(bot)

Dispatcher and Router
---------------------

``examples/dispatcher_router.py`` shows a real router tree. Two child routers
are registered on a ``Dispatcher`` and each owns its own handlers. This is the
pattern to use when an application grows beyond a single flat bot router.

.. code-block:: python

   from peyk import Bot, Dispatcher, Router, F

   bot = Bot("TOKEN", platform="telegram")
   dp = Dispatcher()
   messages = Router(name="messages")
   admin = Router(name="admin")

   @messages.message(F.text)
   async def echo(message):
       await message.answer(f"echo: {message.text}")

   @admin.command("admin")
   async def admin_command(message):
       await message.answer("Admin router handled /admin")

   dp.include_router(messages)
   dp.include_router(admin)
   dp.run_polling(bot)

This also makes the dispatcher boundary explicit: updates are polled by the
``Dispatcher`` and matched against the included router tree.

More examples
-------------

The repository ``examples/`` directory also contains examples for formatting,
keyboards, webhooks, error handling, i18n, filters, and multi-platform bots.
