import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db import init_db
from states import AddServer
from handlers.start import start
from handlers.add_server import (
    add_server_start,
    add_name,
    add_ip,
    add_port,
    add_token
)
from handlers.servers import servers
from handlers.server_menu import open_server
from aiogram import F
from handlers.status import server_status

from handlers.actions_menu import open_actions
from handlers.actions import restart_service, upload_file, view_logs
from handlers.back import back_to_server
from aiogram import F
from handlers.upload import handle_upload
from states import UploadFile
from handlers.test_alert import test_alert

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start, Command("start"))
    dp.message.register(add_server_start, Command("add_server"))
    dp.message.register(add_name, AddServer.name)
    dp.message.register(add_ip, AddServer.ip)
    dp.message.register(add_port, AddServer.port)
    dp.message.register(add_token, AddServer.token)
    dp.message.register(servers, Command("servers"))
    dp.callback_query.register(open_server, F.data.startswith("server:"))
    dp.callback_query.register(server_status, F.data.startswith("status:"))
    dp.callback_query.register(open_actions, F.data.startswith("actions:"))

    dp.callback_query.register(restart_service, F.data.startswith("restart:"))
    dp.callback_query.register(upload_file, F.data.startswith("upload:"))
    dp.callback_query.register(view_logs, F.data.startswith("logs:"))

    dp.callback_query.register(back_to_server, F.data.startswith("back:"))

    dp.message.register(handle_upload, UploadFile.waiting_file)
    dp.message.register(test_alert, Command("test_alert"))


    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())