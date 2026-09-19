"""A complete scene-style registration flow built from StatesGroup + FSMContext."""
from peyk import Bot, Dispatcher
from peyk.filters import StateFilter
from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup


class Registration(StatesGroup):
    name = State()
    email = State()
    done = State()


storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)
bot = Bot("TOKEN", platform="telegram")


@dispatcher.command("register")
async def register(message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer("Registration started. What is your name?")


@dispatcher.message(StateFilter(Registration.name))
async def registration_name(message, state: FSMContext):
    await state.update_data(name=message.text or "")
    await state.set_state(Registration.email)
    await message.answer("What is your email?")


@dispatcher.message(StateFilter(Registration.email))
async def registration_email(message, state: FSMContext):
    data = await state.update_data(email=message.text or "")
    await state.set_state(Registration.done)
    await message.answer(
        f"Registration complete: {data['name']} <{data['email']}>"
    )
    await state.clear()


if __name__ == "__main__":
    dispatcher.run_polling(bot)
