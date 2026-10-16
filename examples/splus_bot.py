"""Minimal Soroush Plus (Splus) bot: a /start keyboard, a callback and an echo.

Run with a token from the Splus bot father::

    SPLUS_TOKEN=... python examples/splus_bot.py
"""
import os

from peyk import SplusBot
from peyk.keyboard import InlineKeyboardBuilder

bot = SplusBot(os.environ["SPLUS_TOKEN"])
keyboard = (InlineKeyboardBuilder()
            .button(text="Say hi", callback_data="hi")
            .button(text="Soroush Plus", url="https://soroushplus.com")
            .adjust(2)
            .as_markup())

@bot.command("start")
async def start(message):
    await message.answer("Hello from peyk on Splus!", reply_markup=keyboard)

@bot.callback_query()
async def on_button(query):
    await query.answer("Hi!")

@bot.message()
async def echo(message):
    if message.text:
        await message.answer(message.text)

if __name__ == "__main__":
    bot.run()
