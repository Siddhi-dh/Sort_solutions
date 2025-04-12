from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from datetime import datetime, timedelta
import pandas as pd
import os
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "FastAPI Pomodoro App is running!"}


# CSV file to store work sessions
CSV_FILE = "work_sessions.csv"

# Create the CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["task_id", "start_time", "end_time", "type"])
    df.to_csv(CSV_FILE, index=False)

# Request model for Pomodoro
class PomodoroRequest(BaseModel):
    duration: int = 25  # default 25 minutes

# WebSocket manager to handle multiple clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, task_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[task_id] = websocket

    def disconnect(self, task_id: str):
        self.active_connections.pop(task_id, None)

    async def send_message(self, task_id: str, message: str):
        if task_id in self.active_connections:
            websocket = self.active_connections[task_id]
            await websocket.send_text(message)

manager = ConnectionManager()

@app.post("/tasks/{task_id}/start-pomodoro")
async def start_pomodoro(task_id: str, request: PomodoroRequest):
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=request.duration)

    # Log work session
    log_session(task_id, start_time, end_time, "work")

    # Start background timer and trigger break when done
    asyncio.create_task(pomodoro_timer(task_id, request.duration))

    return {
        "message": f"Pomodoro timer started for {request.duration} minutes.",
        "end_time": end_time.isoformat() + "Z"
    }

# WebSocket endpoint
@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(task_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # wait for any message to keep it alive
    except WebSocketDisconnect:
        manager.disconnect(task_id)

# Timer function
async def pomodoro_timer(task_id: str, duration: int):
    await asyncio.sleep(duration * 60)

    # Notify work session is done
    await manager.send_message(task_id, "Time's up! Take a 5-minute break ")

    # Log break session
    break_start = datetime.utcnow()
    break_end = break_start + timedelta(minutes=5)
    log_session(task_id, break_start, break_end, "break")

    # Wait 5 minutes break
    await asyncio.sleep(5 * 60)

    # Notify break is over
    await manager.send_message(task_id, "✅ Break's over! Ready to focus again?")

# Function to log session into CSV
def log_session(task_id: str, start_time: datetime, end_time: datetime, session_type: str):
    df = pd.read_csv(CSV_FILE)
    df.loc[len(df)] = {
        "task_id": task_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "type": session_type
    }
    df.to_csv(CSV_FILE, index=False)


