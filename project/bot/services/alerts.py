from aiogram import Bot


async def send_alert(bot: Bot, user_id: int, text: str):
    await bot.send_message(
        user_id,
        f"🚨 УВЕДОМЛЕНИЕ\n\n{text}"
    )
