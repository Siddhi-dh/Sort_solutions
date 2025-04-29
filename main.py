from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a data model
class TimeData(BaseModel):
    task_id: str
    start_time: str  # Example: "2025-03-20T09:00:00Z"
    end_time: str  # Example: "2025-03-20T17:00:00Z"

# API to store start & end time
@app.post("/tasks/{task_id}/set-time")
def set_time(task_id: str, data: TimeData):
    return {"message": f"Start and end times recorded for task {task_id}"}
