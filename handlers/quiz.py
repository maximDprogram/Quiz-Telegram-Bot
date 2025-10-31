from aiogram import types, F
from quiz_data import quiz_data
from keyboards import generate_options_keyboard
from database import get_quiz_index, update_quiz_index, save_result

# Временное хранилище очков в памяти
user_scores = {}


async def get_question(message: types.Message, user_id: int):
    current_question_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_question_index]
    correct_index = question_data['correct_option']
    opts = question_data['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(
        f"Вопрос {current_question_index + 1}/{len(quiz_data)}:\n\n{question_data['question']}",
        reply_markup=kb
    )


async def new_quiz(message: types.Message):
    user_id = message.from_user.id
    user_scores[user_id] = 0
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)


async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)


# Правильный ответ
async def right_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_question_index]
    correct_option_text = question_data['options'][question_data['correct_option']]

    # +1 к очкам
    user_scores[user_id] = user_scores.get(user_id, 0) + 1

    await callback.message.answer(f"Ты выбрал: {correct_option_text}\nВерно!")

    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await finish_quiz(callback.message, user_id)


# Неправильный ответ
async def wrong_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    await callback.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_question_index]
    correct_option_text = question_data['options'][question_data['correct_option']]

    await callback.message.answer(
        f"Ты выбрал неправильный вариант.\nПравильный ответ: {correct_option_text}"
    )

    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await finish_quiz(callback.message, user_id)


# Завершение квиза
async def finish_quiz(message: types.Message, user_id: int):
    total_questions = len(quiz_data)
    correct_answers = user_scores.get(user_id, 0)

    await save_result(user_id, correct_answers, total_questions)

    await message.answer(
        f"Квиз завершён!\n\n"
        f"Твой результат: {correct_answers}/{total_questions} правильных ответов"
    )