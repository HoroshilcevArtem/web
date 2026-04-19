from aiogram.fsm.state import State, StatesGroup

class AddServer(StatesGroup):
    name = State()
    ip = State()
    port = State()
    token = State()

class UploadFile(StatesGroup):
    waiting_file = State()
