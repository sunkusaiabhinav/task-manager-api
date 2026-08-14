from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Task Manager FEATURE VERSION")


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"


class Task(TaskCreate):
    id: int
    status: str = "pending"


tasks = []
next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: TaskCreate):
    global next_id

    new_task = Task(
        id=next_id,
        title=task.title,
        description=task.description,
        priority=task.priority,
    )

    tasks.append(new_task)
    next_id += 1

    return new_task


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")

class TaskStatusUpdate(BaseModel):
    status: str


@app.put("/tasks/{task_id}/status")
def update_task_status(task_id: int, status_data: TaskStatusUpdate):
    allowed_statuses = {"pending", "in_progress", "completed"}

    if status_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status",
        )

    for task in tasks:
        if task.id == task_id:
            task.status = status_data.status
            return task

    raise HTTPException(status_code=404, detail="Task not found")