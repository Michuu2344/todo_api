from fastapi import FastAPI, HTTPException
from typing import List
from models import Task, Month
from uuid import uuid4, UUID
from database import create_database,add_task,delete_task, show_all_tasks,show_one_task, edit_task_db


app = FastAPI()
create_database()

@app.get("/")
async def home():
    return {"Hello":"World"}

@app.get("/todos")
async def show_tasks():
    
    return show_all_tasks()
@app.post("/todos")
async def add_tasks(task : Task):
    add_task(task)
    return f"Succesfully added a task named {task}"
@app.get("/todos/{id}")
async def show_task(id : int):
    return show_one_task(id)
   
@app.delete("/todos/{id}")
async def delete_tasks(id :int):
    return delete_task(id)
    

@app.put("/todos/{id}")
async def edit_task(id, edited_task : Task):
    edit_task_db(edited_task,id)