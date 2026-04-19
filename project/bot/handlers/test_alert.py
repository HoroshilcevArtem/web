from aiogram import types


async def test_alert(message: types.Message):
    await message.answer(
        "🚨 УВЕДОМЛЕНИЕ\n\n"
        "CPU сервера превысил 90%\n"
        "Сервер ID: 1"
    )
