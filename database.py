import sqlite3
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
                completed INTEGER DEFAULT 0,
                owner_username TEXT
                )''')
    conn.commit()
    conn.close()

def user_database():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,            
                email TEXT NOT NULL,
                full_name TEXT NOT NULL,
                hashed_password TEXT NOT NULL,
                disabled INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()
def save_to_user_database(username,email,full_name,hashed):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO users (username,email,full_name,hashed_password)
                VALUES (?,?,?,?)''',(username,email,full_name,hashed))
    conn.commit()
    conn.close()
def get_user_from_db(username):
    conn  = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    try:
        cur.execute('''SELECT * FROM users WHERE username = ?''',(username,))
    
        result = cur.fetchone()
        if result is None:
            return None
        
        return {
        "username":result[1],
        "email":result[2],
        "full_name":result[3],
        "hashed_password":result[4],
        "disabled":bool(result[5])
    }
    finally:
        conn.close()
def show_all_tasks(username):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM tasks WHERE owner_username = ?''',(username,))
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
   
def add_task(task,owner_username):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO tasks (name, category, description, month, completed,owner_username)
                VALUES (?,?,?,?,?,?)''',(task.name,task.category,task.description,task.month,task.completed,owner_username))
    conn.commit()
    conn.close()
def delete_task(task_id,owner_username):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''DELETE FROM tasks WHERE id = ? AND owner_username = ? ''',(task_id,owner_username))
    rows = cur.rowcount
    if rows == 0:
        raise HTTPException(status_code=404,detail=f"There is no task with id: {task_id}")
    conn.commit()
    conn.close()
    return f"Deleted a task with id: {task_id}"
def edit_task_db(task,id,owner_username):
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''UPDATE tasks SET name = ?, category = ?, description = ?, month = ?, completed = ? WHERE id = ? AND owner_username = ?''',
                (task.name,task.category,task.description,task.month,task.completed,id,owner_username))
    rows = cur.rowcount
    if rows == 0:
        raise HTTPException(status_code=404,detail="you didnt change anything")
    conn.commit()
    conn.close()
    return f"Succesfully edited a task with id: {id}"
    