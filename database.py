import aiosqlite
from config import DB_NAME


# Создание таблиц
async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_state (
                user_id INTEGER PRIMARY KEY,
                question_index INTEGER
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                correct_answers INTEGER,
                total_questions INTEGER
            )
        ''')

        await db.commit()


# Работа с прогрессом (индекс вопроса)
async def get_quiz_index(user_id: int) -> int:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def update_quiz_index(user_id: int, index: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)',
            (user_id, index)
        )
        await db.commit()


# Работа с результатами
async def save_result(user_id: int, correct_answers: int, total_questions: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_results (user_id, correct_answers, total_questions) VALUES (?, ?, ?)',
            (user_id, correct_answers, total_questions)
        )
        await db.commit()


async def get_result(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT correct_answers, total_questions FROM quiz_results WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result if result else (None, None)