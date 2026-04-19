from aiogram import types
from aiogram.fsm.context import FSMContext
from states import AddServer
from crypto import encrypt
import aiosqlite
from db import DB


async def add_server_start(message: types.Message, state: FSMContext):
    await message.answer("Название сервера:")
    await state.set_state(AddServer.name)


async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("IP сервера:")
    await state.set_state(AddServer.ip)


async def add_ip(message: types.Message, state: FSMContext):
    await state.update_data(ip=message.text)
    await message.answer("Порт агента:")
    await state.set_state(AddServer.port)


async def add_port(message: types.Message, state: FSMContext):
    await state.update_data(port=int(message.text))
    await message.answer("API токен:")
    await state.set_state(AddServer.token)


async def add_token(message: types.Message, state: FSMContext):
    data = await state.get_data()

    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO servers (user_id, name, ip, port, token) VALUES (?, ?, ?, ?, ?)",
            (
                message.from_user.id,
                data["name"],
                data["ip"],
                data["port"],
                encrypt(message.text)
            )
        )
        await db.commit()

    await message.answer("✅ Сервер добавлен")
    await state.clear()
