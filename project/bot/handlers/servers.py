from aiogram import types
from aiogram.filters import Command
import aiosqlite

from db import DB
from keyboards.servers import servers_kb


async def servers(message: types.Message):
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute(
            "SELECT id, name FROM servers WHERE user_id=?",
            (message.from_user.id,)
        )
        rows = await cursor.fetchall()

    if not rows:
        await message.answer("❌ У тебя нет серверов")
        return

    await message.answer(
        "📋 Выбери сервер:",
        reply_markup=servers_kb(rows)
    )
