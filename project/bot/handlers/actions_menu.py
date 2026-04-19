from aiogram import types
from keyboards.actions import actions_kb


async def open_actions(call: types.CallbackQuery):
    server_id = int(call.data.split(":")[1])

    await call.message.edit_text(
        f"⚙️ Действия для сервера ID: {server_id}\nВыбери действие:",
        reply_markup=actions_kb(server_id)
    )
    await call.answer()
