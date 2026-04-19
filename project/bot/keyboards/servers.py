from aiogram.utils.keyboard import InlineKeyboardBuilder


def servers_kb(servers: list):
    kb = InlineKeyboardBuilder()

    for server_id, name in servers:
        kb.button(
            text=f"🖥 {name}",
            callback_data=f"server:{server_id}"
        )

    kb.adjust(1)  # 1 кнопка в строке
    return kb.as_markup()
