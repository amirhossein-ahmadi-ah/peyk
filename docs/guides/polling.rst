Polling
=======

``bot.run()`` is the simple automatic polling entry point. Explicit applications use ``Dispatcher.start_polling`` or ``run_polling``.

.. code-block:: python

   from peyk import Bot, Dispatcher

   bot = Bot("TOKEN", platform="telegram")
   dp = Dispatcher()
   dp.include_router(bot.router)

   if __name__ == "__main__":
       dp.run_polling(bot)

The polling loop owns graceful shutdown and closes bots by default.
