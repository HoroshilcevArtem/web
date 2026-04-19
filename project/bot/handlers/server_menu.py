from aiogram import types
from keyboards.server_menu import server_menu_kb


async def open_server(call: types.CallbackQuery):
    server_id = int(call.data.split(":")[1])

    await call.message.edit_text(
        f"🖥 Сервер ID: {server_id}\nВыбери действие:",
        reply_markup=server_menu_kb(server_id)
    )
    await call.answer()
