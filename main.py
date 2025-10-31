import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from config import API_TOKEN
from database import create_table
from handlers import cmd_start, cmd_quiz, right_answer, wrong_answer, cmd_stats

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация хэндлеров
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_quiz, Command("quiz"))
dp.message.register(cmd_stats, Command("stats"))
dp.message.register(cmd_quiz, F.text == "Начать игру")
dp.callback_query.register(right_answer, F.data == "right_answer")
dp.callback_query.register(wrong_answer, F.data == "wrong_answer")

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())