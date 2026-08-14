from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Task Manager API")


class TaskCreate(BaseModel):
    title: str
    description: str = ""


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