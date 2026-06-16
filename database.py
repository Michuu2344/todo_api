import sqlite3
import json
from fastapi import HTTPException
def create_database():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,  
                month TEXT,
                completed INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()
def show_all_tasks():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM tasks''')
    res = cur.fetchall()
    tasks = []
    for r in res:
        tasks.append({
            "id": r[0],
            "name": r[1],
            "category": r[2],
            "description": r[3],
            "month": r[4],
            "completed": r[5],
        })
    conn.close()
    return tasks
def show_one_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM tasks WHERE id = ? ''',(task_id,))
    res = cur.fetchone()
    conn.close()
    if res is None:
        raise HTTPException(status_code=404,detail=f"There is no task with id: {task_id}")
    
    return {
            "id": res[0],
            "name": res[1],
            "category": res[2],
            "description": res[3],
            "month": res[4],
            "completed": res[5],
    }
   
def add_task(task):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO tasks (name, category, description, month, completed)
                VALUES (?,?,?,?,?)''',(task.name,task.category,task.description,task.month,task.completed))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''DELETE FROM tasks WHERE id = ?''',(task_id,))
    rows = cur.rowcount
    if rows == 0:
        raise HTTPException(status_code=404,detail=f"There is no task with id: {task_id}")
    conn.commit()
    conn.close()

def edit_task_db(task,id):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''UPDATE tasks SET name = ?, category = ?, description = ?, month = ?, completed = ? WHERE id = ?''',
                (task.name,task.category,task.description,task.month,task.completed,id))
    rows = cur.rowcount
    if rows == 0:
        raise HTTPException(status_code=404,detail="you didnt change anything")
    conn.commit()
    conn.close()
    return f"Succesfully edited a task with id: {id}"
    