from aiogram import types
from database import get_result

async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    correct, total = await get_result(user_id)

    if correct is None:
        await message.answer("Ты ещё не проходил квиз\nИспользуй команду /quiz, чтобы начать!")
    else:
        percent = round((correct / total) * 100, 1)
        await message.answer(
            f"Твоя последняя статистика:\n"
            f"Правильных ответов: {correct}\n"
            f"Всего вопросов: {total}\n"
            f"Успешность: {percent}%"
        )