from cryptography.fernet import Fernet
from config import FERNET_KEY

fernet = Fernet(FERNET_KEY.encode())

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
