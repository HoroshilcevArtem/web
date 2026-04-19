from aiogram import types

async def server_status(call: types.CallbackQuery):
    server_id = call.data.split(":")[1]

    # временно — позже будет запрос к агенту
    text = (
        "📊 Статус сервера\n\n"
        "CPU: 23%\n"
        "RAM: 1.2 / 4 GB\n"
        "Disk: 18 / 40 GB\n"
        "Uptime: 3 days\n"
        "Agent: 🟢 Online"
    )

    await call.message.answer(text)
    await call.answer()
