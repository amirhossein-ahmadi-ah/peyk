FSM and scene-style flows
=========================

Peyk provides declarative ``State``/``StatesGroup`` classes and ``FSMContext`` backed by ``MemoryStorage`` or ``RedisStorage``. The project does not expose a separate ``Scene`` class; multi-step scene-style flows are represented by state groups.

.. code-block:: python

   from peyk import Bot
   from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup

   class Form(StatesGroup):
       name = State()
       age = State()

   storage = MemoryStorage()
   bot = Bot("TOKEN", platform="telegram")

   # Dispatcher integrations create FSMContext with a platform-aware StorageKey.

The documented FSM key format is platform + bot ID + conversation identity + destiny; see ``docs/decisions.md``.
