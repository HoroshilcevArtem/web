from fastapi import FastAPI, Header, HTTPException, WebSocket, WebSocketDisconnect
import psutil
import asyncio

from monitor import check_metrics
from config import AGENT_TOKEN

app = FastAPI(title="Server Agent")


# =====================
# AUTH
# =====================
def auth(token: str):
    if token != AGENT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


# =====================
# HTTP ENDPOINTS
# =====================
@app.get("/status")
def status(x_agent_token: str = Header(...)):
    auth(x_agent_token)
    return {"status": "online"}


@app.get("/metrics")
def metrics(x_agent_token: str = Header(...)):
    auth(x_agent_token)
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent
    }


@app.post("/check")
def check(x_agent_token: str = Header(...)):
    auth(x_agent_token)
    check_metrics()
    return {"ok": True}


# =====================
# WEBSOCKET (LIVE METRICS)
# =====================
def get_metrics_ws():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
    }


@app.websocket("/ws/metrics")
async def ws_metrics(ws: WebSocket):
    await ws.accept()

    token = ws.headers.get("x-agent-token")
    if token != AGENT_TOKEN:
        await ws.close(code=1008)
        return

    try:
        while True:
            await ws.send_json(get_metrics_ws())
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
