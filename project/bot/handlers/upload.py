import os
from aiogram import types
from aiogram.fsm.context import FSMContext
from states import UploadFile

UPLOAD_DIR = "uploads"


async def handle_upload(message: types.Message, state: FSMContext):
    if not message.document:
        await message.answer("❌ Это не файл. Отправь document.")
        return

    data = await state.get_data()
    server_id = data["server_id"]

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file = message.document
    file_path = f"{UPLOAD_DIR}/{server_id}_{file.file_name}"

    await message.bot.download(
        file=file.file_id,
        destination=file_path
    )

    await message.answer(
        f"✅ Файл `{file.file_name}` сохранён\n"
        f"Сервер ID: {server_id}"
    )

    await state.clear()
