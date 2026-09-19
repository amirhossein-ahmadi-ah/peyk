"""A complete multi-step FSM conversation using the dispatcher integration."""
from peyk import Bot, Dispatcher
from peyk.filters import StateFilter
from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup


class Form(StatesGroup):
    name = State()
    age = State()


storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)
bot = Bot("TOKEN", platform="telegram")


@dispatcher.command("start")
async def start(message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("What is your name?")


@dispatcher.message(StateFilter(Form.name))
async def name_step(message, state: FSMContext):
    await state.update_data(name=message.text or "")
    await state.set_state(Form.age)
    await message.answer("How old are you?")


@dispatcher.message(StateFilter(Form.age))
async def age_step(message, state: FSMContext):
    data = await state.update_data(age=message.text or "")
    await message.answer(f"Thanks {data['name']}! Your age is {data['age']}.")
    await state.clear()


if __name__ == "__main__":
    dispatcher.run_polling(bot)
