from aiogram import types
from aiogram.fsm.context import FSMContext
from states import UploadFile


async def upload_file(call: types.CallbackQuery, state: FSMContext):
    server_id = int(call.data.split(":")[1])

    await state.update_data(server_id=server_id)
    await state.set_state(UploadFile.waiting_file)

    await call.message.answer(
        f"📁 Сервер ID: {server_id}\n"
        "Отправь файл, который нужно загрузить на сервер"
    )
    await call.answer()


async def restart_service(call: types.CallbackQuery):
    server_id = call.data.split(":")[1]

    await call.message.answer(
        f"🔄 Сервер {server_id}\n"
        "Перезапуск сервиса отправлен (заглушка)"
    )
    await call.answer()


async def upload_file(call: types.CallbackQuery):
    server_id = call.data.split(":")[1]

    await call.message.answer(
        f"📁 Сервер {server_id}\n"
        "Отправь файл для загрузки (скоро)"
    )
    await call.answer()


async def view_logs(call: types.CallbackQuery):
    server_id = call.data.split(":")[1]

    await call.message.answer(
        f"📄 Логи сервера {server_id}\n"
        "Последние 50 строк (заглушка)"
    )
    await call.answer()
