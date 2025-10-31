from aiogram import types
from aiogram.filters.command import Command
from keyboards import start_keyboard

async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=start_keyboard())