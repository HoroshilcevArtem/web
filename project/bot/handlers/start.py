from aiogram import types

async def start(message: types.Message):
    await message.answer(
        "👋 DevOps Bot\n\n"
        "/add_server — добавить сервер\n"
        "/servers — список серверов"
    )
