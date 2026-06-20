from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm  
from models import TaskCreate,Task, Month, UserRegister, TaskEdit, Token, TokenData,User,UserInDB
from uuid import uuid4, UUID
from database import create_database,add_task,delete_task, show_all_tasks,show_one_task, edit_task_db, user_database,save_to_user_database, get_user_from_db
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

SECRET_KEY = "61c7bb6af8f2a93c32580b915ae425e4a95ecc8da60b1d0ae7aa6ae5e70e635c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


create_database()
user_database()


password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def get_user(username :str) -> UserInDB | None:
    
    user = get_user_from_db(username)
    if user is None:
        return None
    return UserInDB(**user)
def authenticate_user(username :str,password :str):
    user = get_user(username)
    if not user:
        verify_password(password,DUMMY_HASH)
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user
def create_access_token(data :dict,expires_delta :timedelta| None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentils",
            headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username = token_data.username)
    if user is None:
        raise credentials_exception
    return user
async def get_current_active_user(current_user :Annotated[User,Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
)->Token:
    user = authenticate_user(form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)
    return Token(access_token= access_token,token_type="bearer")
  
@app.get("/users/me/")
async def read_users_me(current_user: Annotated[User,Depends(get_current_active_user)])-> User:
    return current_user
@app.get("/users")
async def users(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token":token}
@app.post("/auth/register")
async def register_user(user: UserRegister):
    hashed = get_password_hash(user.password)
    save_to_user_database(user.username,user.email,user.full_name,hashed)
    return {"message": f"User {user.username} registered successfully"}
@app.get("/todos")
async def show_tasks(current_user: Annotated[User, Depends(get_current_active_user)]):
    return show_all_tasks(current_user.username)
@app.post("/todos")
async def add_tasks(task : TaskCreate,current_user: Annotated[User, Depends(get_current_active_user)]):
    add_task(task,current_user.username)
    return f"Succesfully added a task named {task.name}"
@app.get("/todos/{id}")
async def show_task(id : int):
    return show_one_task(id)
   
@app.delete("/todos/{id}")
async def delete_tasks(id :int,current_user : Annotated[User, Depends(get_current_active_user)]):
    return delete_task(id,current_user.username)
    

@app.put("/todos/{id}")
async def edit_task(id, edited_task : TaskEdit,current_user : Annotated[User,Depends(get_current_active_user)]):
    return edit_task_db(edited_task,id,current_user.username)