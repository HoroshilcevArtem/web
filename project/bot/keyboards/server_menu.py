from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def server_menu_kb(server_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Статус",
                    callback_data=f"status:{server_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Действия",
                    callback_data=f"actions:{server_id}"
                )
            ]
        ]
    )
