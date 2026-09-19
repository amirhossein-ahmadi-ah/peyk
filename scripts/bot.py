"""Multi-platform registration example using one Router + Dispatcher + FSM."""
from __future__ import annotations

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from peyk import Bot, Dispatcher, F, Router
from peyk.filters import CallbackDataEquals, Command, StateFilter
from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup


class Registration(StatesGroup):
    """States for the small cross-platform registration flow."""

    name = State()
    age = State()
    confirm = State()


router = Router(name="registration")


@router.message(Command("start", prefix="/"))
async def start(message, state: FSMContext) -> None:
    """Reset the conversation and show the registration command."""
    await state.clear()
    await message.answer("Welcome! Send /register to start.")


@router.message(Command("register", prefix="/"))
async def register(message, state: FSMContext) -> None:
    """Start collecting the user's name."""
    await state.set_state(Registration.name)
    await message.answer("What is your name?")


@router.message(StateFilter(Registration.name))
async def name_step(message, state: FSMContext) -> None:
    """Store the name and request an age."""
    await state.update_data(name=message.text or "")
    await state.set_state(Registration.age)
    await message.answer("How old are you?")


@router.message(StateFilter(Registration.age))
async def age_step(message, state: FSMContext) -> None:
    """Validate and store the age before confirmation."""
    try:
        age = int(message.text or "")
    except ValueError:
        await message.answer("Please send a number.")
        return
    if age < 1 or age > 150:
        await message.answer("Please send an age from 1 to 150.")
        return
    await state.update_data(age=age)
    await state.set_state(Registration.confirm)
    await message.answer("Send /confirm to finish or /cancel to stop.")


@router.message(Command("confirm", prefix="/"), StateFilter(Registration.confirm))
async def confirm(message, state: FSMContext) -> None:
    """Finish the registration and clear its FSM state."""
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Registered {data.get('name', 'user')} ({data.get('age')}).")


@router.message(Command("cancel", prefix="/"))
async def cancel(message, state: FSMContext) -> None:
    """Cancel and clear the current registration."""
    await state.clear()
    await message.answer("Registration cancelled.")


@router.callback_query(CallbackDataEquals("reg_confirm"), StateFilter(Registration.confirm))
async def callback_confirm(callback, state: FSMContext) -> None:
    """Finish the same registration flow from an inline callback."""
    data = await state.get_data()
    await state.clear()
    if callback.message is not None:
        await callback.message.answer(f"Registered {data.get('name', 'user')} ({data.get('age')}).")
    await callback.answer()


def build_bots() -> list[Bot[object]]:
    """Create all configured platform bots without exposing platform to handlers."""
    bots: list[Bot[object]] = []
    for env_name, platform in (
        ("TELEGRAM_BOT_TOKEN", "telegram"),
        ("BALE_BOT_TOKEN", "bale"),
        ("RUBIKA_BOT_TOKEN", "rubika"),
    ):
        token = os.getenv(env_name)
        if token:
            bots.append(Bot(token, platform=platform))
    return bots


async def main() -> None:
    """Run every configured platform through the same dispatcher and router."""
    bots = build_bots()
    if not bots:
        raise RuntimeError("Set at least one bot token environment variable.")
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(router)
    await dispatcher.start_polling(*bots)


if __name__ == "__main__":
    asyncio.run(main())
