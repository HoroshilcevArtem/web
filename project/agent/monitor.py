import psutil
import requests
from config import *

def send_alert(alert_type: str, message: str):
    requests.post(
        BOT_ALERT_URL,
        json={
            "token": AGENT_TOKEN,
            "server_id": SERVER_ID,
            "type": alert_type,
            "message": message
        },
        timeout=5
    )


def check_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    if cpu > CPU_LIMIT:
        send_alert("cpu", f"CPU нагрузка {cpu}%")

    if ram > RAM_LIMIT:
        send_alert("ram", f"RAM использование {ram}%")

    if disk > DISK_LIMIT:
        send_alert("disk", f"DISK заполнен на {disk}%")
