from aiogram.utils.keyboard import InlineKeyboardBuilder


def actions_kb(server_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="🔄 Перезапуск сервиса", callback_data=f"restart:{server_id}")
    kb.button(text="📁 Загрузить файл", callback_data=f"upload:{server_id}")
    kb.button(text="📄 Логи", callback_data=f"logs:{server_id}")
    kb.button(text="🔙 Назад", callback_data=f"back:{server_id}")

    kb.adjust(1)
    return kb.as_markup()
