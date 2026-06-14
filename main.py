from fastapi import FastAPI, HTTPException
from typing import List
from models import Task, Month
from uuid import uuid4, UUID
app = FastAPI()
db: List[Task] = [Task(id = uuid4(),
                  name = "See a doctor",
                  category = "health",
                  description="My ankle hurts",
                  month = "june"),
                  Task(id = uuid4(),
                  name = "Mechanic",
                  category = "car",
                  description="I hear knocking in my suspension",
                  month = "july")]
@app.get("/")
async def home():
    return {"Hello":"World"}

@app.get("/todos")
async def show_tasks():
        return db
@app.post("/todos")
async def add_tasks(task : Task):
      db.append(task)
      return f"Succesfully added a task named: {task.name}"
@app.get("/todos/{id}")
async def show_task(id : UUID):
    for task in db:
            if task.id == id:
                return task
    raise HTTPException(
            status_code=404,
            detail=f"There is no task with id: {id}"
            )
@app.delete("/todos/{id}")
async def delete_task(id : UUID):
    for task in db:
        if task.id == id:
            db.remove(task)
            return f"Succesfully deleted a task named: {task.name}"
    raise HTTPException(
                status_code=404,
                detail=f"There is no task with id: {id}"
            )
@app.put("/todos/{id}")
async def edit_task(id :UUID, edited_task : Task):
    for task in db:
        if task.id == id:    
            if edited_task.name is not None:
                task.name = edited_task.name
            if edited_task.category is not None:
                task.category = edited_task.category
            if edited_task.description is not None:
                task.description = edited_task.description
            if edited_task.month is not None:
                task.month = edited_task.month
            return
    raise HTTPException(
                status_code=404,
                detail=f"There is no task with id: {id}"
            )    
