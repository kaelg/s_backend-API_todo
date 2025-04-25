from re import search
from xmlrpc.client import Boolean

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: str

class Tasks(BaseModel):
    tasks: List[Task]

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*'],
)


memory_db = {"tasks": []}
memory_db["tasks"].append(Task(title="asd",description="desc",status="statuus",priority="prior"))

@app.get("/tasks",response_model=Tasks)
def get_tasks():
    return Tasks(tasks=memory_db["tasks"])


@app.post("/tasks",response_model=Task)
def add_task(task: Task):
    memory_db["tasks"].append(task)
    return {"tasks": f"tasks '{task}' added successfully!"}

@app.delete("/tasks", response_model=Boolean)
def delete_task_by_title(text: str):
    for task in memory_db["tasks"]:
        if task.title == text:
            memory_db["tasks"].remove(task)
            return True
    return False


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)